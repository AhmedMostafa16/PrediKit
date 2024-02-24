import asyncio
from concurrent.futures import ThreadPoolExecutor
import functools
import gc
import logging
import multiprocessing
import sys
import traceback
from json import dumps as stringify
from typing import Any, Dict, List, Optional, TypedDict
import importlib
import os

# pylint: disable=unused-import
from sanic import Sanic
from sanic.log import logger, access_logger
from sanic.request import Request
from sanic.response import json
from sanic_cors import CORS
from asyncio_locked_dict import AsyncioLockedDict

from nodes.node_factory import NodeFactory

from base_types import NodeId, InputId, OutputId
from chain.cache import OutputCache
from chain.json import parse_json, JsonNode
from chain.optimize import optimize
from events import EventQueue, ExecutionErrorData
from process import Executor, NodeExecutionError, timed_supplier
from progress import Aborted  # type: ignore
from response import (
    errorResponse,
    alreadyRunningResponse,
    noExecutorResponse,
    successResponse,
)
from nodes.nodes.builtin_categories import category_order

missing_node_count = 0
categories = set()
missing_categories = set()

# Dynamically import all nodes
for root, dirs, files in os.walk(
    os.path.join(os.path.dirname(__file__), "nodes", "nodes")
):
    for file in files:
        if file.endswith(".py") and not file.startswith("_"):
            module = os.path.relpath(
                os.path.join(root, file), os.path.dirname(__file__)
            )
            module = module.replace(os.path.sep, ".")[:-3]
            try:
                importlib.import_module(f"{module}", package=None)
            except ImportError as e:
                missing_node_count += 1
                logger.warning(f"Failed to import {module}: {e}")

                # Turn path into __init__.py path
                init_module = module.split(".")
                init_module[-1] = "__init__"
                init_module = ".".join(init_module)
                try:
                    category = getattr(
                        importlib.import_module(init_module), "category"
                    )
                    missing_categories.add(category.name)
                except ImportError as ie:
                    logger.warning(ie)
        # Load categories from __init__.py files
        elif file.endswith(".py") and file == ("__init__.py"):
            module = os.path.relpath(
                os.path.join(root, file), os.path.dirname(__file__)
            )
            module = module.replace(os.path.sep, ".")[:-3]
            try:
                # TODO: replace the category system with a dynamic factory
                category = getattr(importlib.import_module(module), "category")
                categories.add(category)
            except:
                pass


categories = sorted(
    list(categories), key=lambda category: category_order.index(category.name)
)


class AppContext:
    """
    Represents the application context.

    Attributes:
        executors (Dict[str, Executor]): A dictionary of executors.
        cache (Dict[NodeId, Any]): A dictionary used for caching.
        queue (EventQueue): An event queue.
        pool (ThreadPoolExecutor): A thread pool executor.
    """

    def __init__(self):
        self.executors: Dict[str, Executor] = AsyncioLockedDict()
        self.cache: Dict[NodeId, Any] = AsyncioLockedDict()
        # This will be initialized by setup_queue.
        # This is necessary because we don't know Sanic's event loop yet.
        self.queue: EventQueue = None  # type: ignore
        self.pool = ThreadPoolExecutor(
            max_workers=multiprocessing.cpu_count() // 2
        )

    @staticmethod
    def get(app_instance: Sanic) -> "AppContext":
        assert isinstance(app_instance.ctx, AppContext)
        return app_instance.ctx


app = Sanic("PrediKit", ctx=AppContext())
app.config.REQUEST_TIMEOUT = sys.maxsize
app.config.RESPONSE_TIMEOUT = sys.maxsize
CORS(app)


class SSEFilter(logging.Filter):
    def filter(self, record):
        return not (record.request.endswith("/sse") and record.status == 200)  # type: ignore


class ZeroCounter:
    """
    A class that keeps track of the number of times it has been entered and exited.

    This class is used to keep track of the number of times it has been entered and exited.
    It is used to ensure that the count is zero before continuing. This is useful for ensuring
    that all previews have been completed before running the nodes. It is also useful for
    ensuring that all nodes have been run before continuing. This class is used as a context
    manager and can be used with the `with` statement.
    """

    def __init__(self) -> None:
        self.count = 0

    async def wait_zero(self) -> None:
        """
        Asynchronously waits until the count becomes zero.
        """
        while self.count != 0:
            await asyncio.sleep(0.01)

    def __enter__(self):
        """
        Increments the count when entering a context.
        """
        self.count += 1

    def __exit__(self, _exc_type, _exc_value, _exc_traceback):
        """
        Decrements the count when exiting a context.
        """
        self.count -= 1


# This counter is used to ensure that all previews have been completed before running the nodes.
runIndividualCounter = ZeroCounter()

# Add a filter to the access logger to filter out successful SSE requests
access_logger.addFilter(SSEFilter())


@app.route("/workflows/<workflow_id:str>/nodes")
async def nodes(_):
    """Gets a list of all nodes as well as the node information"""
    registry = NodeFactory.get_registry()
    logger.debug(categories)

    # sort nodes in category order
    sorted_registry = sorted(
        registry.items(),
        key=lambda x: category_order.index(
            NodeFactory.get_node(x[0]).category.name
        ),
    )
    node_list = []
    for schema_id, _node_class in sorted_registry:
        node_object = NodeFactory.get_node(schema_id)
        node_dict = {
            "schemaId": schema_id,
            "name": node_object.name,
            "category": node_object.category.name,
            "inputs": [x.toDict() for x in node_object.inputs],
            "outputs": [x.toDict() for x in node_object.outputs],
            "description": node_object.description,
            "icon": node_object.icon,
            "subcategory": node_object.sub,
            "nodeType": node_object.type,
            "hasSideEffects": node_object.side_effects,
            "deprecated": node_object.deprecated,
        }
        if node_object.type == "iterator":
            node_dict["defaultNodes"] = node_object.get_default_nodes()  # type: ignore
        node_list.append(node_dict)
    return json(
        {
            "nodes": node_list,
            "categories": [x.toDict() for x in categories],
            "categoriesMissingNodes": list(missing_categories),
        }
    )


class RunRequest(TypedDict):
    data: List[JsonNode]


@app.route("/workflows/<workflow_id:str>/run", methods=["POST"])
async def run(request: Request, workflow_id: str):
    """Runs the provided nodes"""
    ctx = AppContext.get(request.app)
    if workflow_id in ctx.executors:
        if ctx.executors[workflow_id].is_running():
            return json(
                alreadyRunningResponse("Workflow is already running!"),
                status=400,
            )
        if ctx.executors[workflow_id].is_paused():
            ctx.executors[workflow_id].resume()
            return json(
                successResponse("Successfully resumed execution!"), status=201
            )

    try:
        # wait until all previews are done
        await runIndividualCounter.wait_zero()

        full_data: RunRequest = dict(request.json)  # type: ignore
        logger.info(full_data)
        chain, inputs = parse_json(full_data["data"])
        optimize(chain)

        logger.info("Running new executor...")

        executor = Executor(
            chain,
            inputs,
            app.loop,
            ctx.queue,
            ctx.pool,
            parent_cache=OutputCache(static_data=ctx.cache.copy()),
        )
        try:
            ctx.executors[workflow_id] = executor
            await executor.run()
        except Aborted:
            pass
        finally:
            del ctx.executors[workflow_id]
            # gc.collect()

        await ctx.queue.put(
            {"event": "finish", "data": {"message": "Successfully ran nodes!"}}
        )
        return json(successResponse("Successfully ran nodes!"), status=200)
    except Exception as exception:
        logger.error(exception, exc_info=True)
        logger.error(traceback.format_exc())

        error: ExecutionErrorData = {
            "message": "Error running nodes!",
            "source": None,
            "exception": str(exception),
        }
        if isinstance(exception, NodeExecutionError):
            error["source"] = {
                "nodeId": exception.node.id,
                "schemaId": exception.node.schema_id,
                "inputs": exception.inputs,
            }

        await ctx.queue.put({"event": "execution-error", "data": error})
        return json(
            errorResponse("Error running nodes!", exception), status=500
        )


class RunIndividualRequest(TypedDict):
    id: NodeId
    inputs: List[Any]
    schemaId: str


@app.route("/workflows/<workflow_id:str>/run/individual", methods=["POST"])
async def run_individual(request: Request):
    """Runs a single node"""
    ctx = AppContext.get(request.app)
    try:
        full_data: RunIndividualRequest = dict(request.json)  # type: ignore
        if ctx.cache.get(full_data["id"], None) is not None:
            del ctx.cache[full_data["id"]]
        logger.info(full_data)

        # Create node based on given category/name information
        node_instance = NodeFactory.get_node(full_data["schemaId"])

        # Enforce that all inputs match the expected input schema
        enforced_inputs = []
        if node_instance.type == "iteratorHelper":
            enforced_inputs = full_data["inputs"]
        else:
            node_inputs = node_instance.inputs
            for idx, node_input in enumerate(full_data["inputs"]):
                enforced_inputs.append(node_inputs[idx].enforce_(node_input))

        with runIndividualCounter:
            # Run the node and pass in inputs as args
            run_func = functools.partial(
                node_instance.run, *full_data["inputs"]
            )
            output, execution_time = await app.loop.run_in_executor(
                None, timed_supplier(run_func)
            )

            # Cache the output of the node
            ctx.cache[full_data["id"]] = output

        # Broadcast the output from the individual run
        broadcast_data: Dict[OutputId, Any] = dict()
        node_outputs = node_instance.outputs
        if len(node_outputs) > 0:
            output_idxable = [output] if len(node_outputs) == 1 else output
            for idx, node_output in enumerate(node_outputs):
                try:
                    broadcast_data[node_output.id] = (
                        node_output.get_broadcast_data(output_idxable[idx])
                    )
                except Exception as error:
                    logger.error(f"Error broadcasting output: {error}")
            await ctx.queue.put(
                {
                    "event": "node-finish",
                    "data": {
                        "finished": [],
                        "nodeId": full_data["id"],
                        "executionTime": execution_time,
                        "data": broadcast_data,
                    },
                }
            )
        del node_instance, run_func
        # gc.collect()
        return json({"success": True, "data": None})
    except Exception as exception:
        logger.error(exception, exc_info=True)
        return json({"success": False, "error": str(exception)})


@app.route(
    "/workflows/<workflow_id:str>/clearcache/individual", methods=["POST"]
)
async def clear_cache_individual(request: Request):
    ctx = AppContext.get(request.app)
    try:
        full_data = dict(request.json)  # type: ignore
        if ctx.cache.get(full_data["id"], None) is not None:
            del ctx.cache[full_data["id"]]
        return json({"success": True, "data": None})
    except Exception as exception:
        logger.error(exception, exc_info=True)
        return json({"success": False, "error": str(exception)})


@app.get("/sse")
async def sse(request: Request):
    ctx = AppContext.get(request.app)
    headers = {"Cache-Control": "no-cache"}
    response = await request.respond(
        headers=headers, content_type="text/event-stream"
    )
    while True:
        message = await ctx.queue.get()
        if response is not None:
            await response.send(f"event: {message['event']}\n")
            await response.send(f"data: {stringify(message['data'])}\n\n")


@app.after_server_start
async def setup_queue(sanic_app: Sanic, _):
    AppContext.get(sanic_app).queue = EventQueue()


@app.route("/workflows/<workflow_id:str>/pause", methods=["POST"])
async def pause(request: Request, workflow_id: str):
    """Pauses the current execution"""
    ctx = AppContext.get(request.app)

    if not workflow_id in ctx.executors:
        message = "No executor to pause"
        logger.warning(message)
        return json(noExecutorResponse(message), status=400)

    try:
        logger.info("Executor found. Attempting to pause...")
        ctx.executors[workflow_id].pause()
        return json(
            successResponse("Successfully paused execution!"), status=201
        )
    except Exception as exception:
        logger.log(2, exception, exc_info=True)
        return json(
            errorResponse("Error pausing execution!", exception), status=500
        )


@app.route("/workflows/<workflow_id:str>/resume", methods=["POST"])
async def resume(request: Request, workflow_id: str):
    """Pauses the current execution"""
    ctx = AppContext.get(request.app)

    if not workflow_id in ctx.executors:
        message = "No executor to resume"
        logger.warning(message)
        return json(noExecutorResponse(message), status=400)

    try:
        logger.info("Executor found. Attempting to resume...")
        ctx.executors[workflow_id].resume()
        return json(
            successResponse("Successfully resumed execution!"), status=201
        )
    except Exception as exception:
        logger.log(2, exception, exc_info=True)
        return json(
            errorResponse("Error resuming execution!", exception), status=500
        )


@app.route("/workflows/<workflow_id:str>/kill", methods=["POST"])
async def kill(request: Request, workflow_id: str):
    """Kills the current execution"""
    ctx = AppContext.get(request.app)

    if not workflow_id in ctx.executors:
        message = "No executor to kill"
        logger.warning("No executor to kill")
        return json(noExecutorResponse(message), status=400)

    try:
        logger.info("Executor found. Attempting to kill...")
        ctx.executors[workflow_id].kill()
        return json(
            successResponse("Successfully killed execution!"), status=201
        )
    except Exception as exception:
        logger.log(2, exception, exc_info=True)
        return json(
            errorResponse("Error killing execution!", exception), status=500
        )


if __name__ == "__main__":
    host: str = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 5001))
    workers = int(os.getenv("WORKERS", multiprocessing.cpu_count()))
    is_production: bool = (
        os.environ.get("Production", "True").lower() == "true"
    )

    # Ensure at least one worker is running
    if workers < 1 and not is_production:
        workers = 1
    else:
        workers = multiprocessing.cpu_count()

    app.run(
        host=host,
        port=port,
        workers=workers,
        debug=not is_production,
        access_log=is_production,
        auto_reload=not is_production,
    )
