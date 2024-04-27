import asyncio
from concurrent.futures import ThreadPoolExecutor
import functools
import gc
import importlib
from json import dumps as stringify
import logging
import multiprocessing
import os
import sys
import traceback
import pandas
from typing import (
    Any,
    Dict,
    List,
    TypedDict,
)

from asyncio_locked_dict import AsyncioLockedDict
from base_types import (
NodeId,
    OutputId,
)
from bson import ObjectId
from chain.cache import OutputCache
from chain.json import (
    JsonNode,
    parse_json,
)
from chain.optimize import optimize
from dotenv import load_dotenv
from events import (
    EventQueue,
    ExecutionErrorData,
)
from motor.motor_asyncio import AsyncIOMotorClient
from nodes.node_factory import NodeFactory
from nodes.nodes.builtin_categories import category_order
from process import (
    Executor,
    NodeExecutionError,
    timed_supplier,
)
from progress import Aborted  # type: ignore
from response import (
    alreadyRunningResponse,
    errorResponse,
    noExecutorResponse,
    successResponse,
)
from sanic import Sanic
from sanic.log import (
    access_logger,
    logger,
)
from sanic.request import Request
from sanic.response import json

# pylint: disable=unused-import, wrong-import-position
root = os.path.dirname(os.path.abspath("../predikit/"))
sys.path.append(root)

# pylint: disable=unused-import


dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


# Set up counters
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
# CORS(app)

# Set up MongoDB
mongodb_url = os.getenv("MONGODB_CONNECTION_STRING")
logger.info(f"Connecting to MongoDB at {mongodb_url}")
client = AsyncIOMotorClient(mongodb_url)

# Set up the database
db = client.predikit
workflows_collection = db.workflows


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


@app.route("/workflows/nodes")
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
                successResponse("Successfully resumed execution!"), status=200
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
            ctx.cache.update(executor.cache.get_all())
            del ctx.executors[workflow_id]
            gc.collect()

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
        logger.warning(message + "!\n" + str(request.json))
        return json(noExecutorResponse(message), status=400)

    try:
        logger.info("Executor found. Attempting to pause...")
        ctx.executors[workflow_id].pause()
        return json(
            successResponse("Successfully paused execution!"), status=200
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
        logger.warning(message + "!\n" + str(request.json))
        return json(noExecutorResponse(message), status=400)

    try:
        logger.info("Executor found. Attempting to resume...")
        ctx.executors[workflow_id].resume()
        return json(
            successResponse("Successfully resumed execution!"), status=200
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
        logger.warning(message + "!\n" + str(request.json))
        return json(noExecutorResponse(message), status=400)

    try:
        logger.info("Executor found. Attempting to kill...")
        ctx.executors[workflow_id].kill()
        return json(
            successResponse("Successfully killed execution!"), status=200
        )
    except Exception as exception:
        logger.log(2, exception, exc_info=True)
        return json(
            errorResponse("Error killing execution!", exception), status=500
        )


@app.route("/ping", methods=["GET"])
async def ping(_):
    return json(successResponse("Pong"), status=200)


@app.route("/workflows", methods=["GET"])
async def get_all_workflows(_):
    try:
        workflows = await workflows_collection.find().to_list(None)
        for workflow in workflows:
            workflow["id"] = str(workflow["_id"])
            del workflow["_id"]
        return json(workflows, status=200)
    except Exception as e:
        return json(errorResponse("Error fetching workflows!", e), status=500)


@app.route("/workflows", methods=["POST"])
async def create_workflow(request: Request):
    try:
        workflow = request.json
        result = await workflows_collection.insert_one(workflow)
        return json(successResponse(str(result.inserted_id)), status=201)
    except Exception as e:
        return json(errorResponse("Error creating workflow!", e), status=500)


@app.route("/workflows/<workflow_id:str>", methods=["GET"])
async def get_workflow(request: Request, workflow_id: str):
    try:
        workflow = await workflows_collection.find_one(
            {"_id": ObjectId(workflow_id)}
        )
        if workflow:
            workflow["id"] = str(workflow["_id"])
            del workflow["_id"]
            return json(workflow, status=200)
        return json(errorResponse("Workflow not found!", ""), status=404)
    except Exception as e:
        return json(errorResponse("Error fetching workflow!", e), status=500)


@app.route("/workflows/<workflow_id:str>", methods=["PUT"])
async def update_workflow(request: Request, workflow_id: str):
    try:
        workflow = request.json
        result = await workflows_collection.replace_one(
            {"_id": ObjectId(workflow_id)}, workflow
        )
        if result.matched_count == 0:
            return json(errorResponse("Workflow not found!", ""), status=404)
        if result.modified_count == 0:
            return json(errorResponse("Workflow not updated!", ""), status=500)
        return json(successResponse(""), status=200)
    except Exception as e:
        return json(errorResponse("Error updating workflow!", e), status=500)


@app.route("/workflows/<workflow_id:str>", methods=["DELETE"])
async def delete_workflow(request: Request, workflow_id: str):
    try:
        result = await workflows_collection.delete_one({"_id": workflow_id})
        if result.deleted_count == 0:
            return json(errorResponse("Workflow not found!", ""), status=404)
        return json(successResponse(""), status=200)
    except Exception as e:
        return json(errorResponse("Error deleting workflow!", e), status=500)


@app.route("/workflows/<workflow_id:str>/preview", methods=["POST"])
async def preview_node(request: Request, workflow_id: str):
    """Returns the output of a single node"""
    ctx = AppContext.get(request.app)
    PAGE_SIZE = 1000
    try:
        full_data: RunIndividualRequest = dict(request.json)  # type: ignore
        logger.info(full_data)

        # If the node is already in the cache, return the cached data
        # Otherwise, return an error
        df = pandas.DataFrame()
        if full_data["id"] in ctx.cache:
            node = ctx.cache[full_data["id"]]
            if isinstance(node, tuple):
                # try to find the dataframe in the tuple elements
                for element in node:
                    if isinstance(element, pandas.DataFrame):
                        df = element
                        break
            elif isinstance(node, pandas.DataFrame):
                df = node
            else:
                return json(
                    {
                        "success": False,
                        "error": "Node output is not a Dataset.",
                    }
                )
                
            page = full_data.get("page", 1)
            start = (page - 1) * PAGE_SIZE
            end = page * PAGE_SIZE
            return json(
                {
                    "success": True,
                    # "data": df[start:end].to_dict(orient="records"),
                    "data": df[start:end].to_json(orient="records"),
                }
            )
        else:
            return json(
                {
                    "success": False,
                    "error": "Run the workflow first.",
                }
            )
    except Exception as exception:
        logger.error(exception, exc_info=True)
        return json({"success": False, "error": str(exception)})


# Main entry point for the application
if __name__ == "__main__":
    host: str = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 5001))
    workers = int(os.getenv("WORKERS", multiprocessing.cpu_count()))
    is_production: bool = (
        os.environ.get("Production", "True").lower() == "true"
    )

    # Ensure at least one worker is running
    if workers < 1 and not is_production:
        logger.info("Setting workers to 1")
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