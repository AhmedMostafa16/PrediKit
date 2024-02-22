import asyncio
import functools
import logging
import multiprocessing
import os
import sys
import traceback
from json import dumps as stringify
from typing import Any
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


# pylint: disable=unused-import
from sanic import Sanic
from sanic.log import logger, access_logger
from sanic.request import Request
from sanic.response import json
from sanic_cors import CORS
from backend.concurrencysafe_dict import ConcurrencySafeDict

from nodes.categories import category_order


# pylint: disable=unused-import
from nodes.node_factory import NodeFactory
from process import Executor

load_dotenv(".env")

# Retrieve MongoDB connection string from environment variables
MONGO_URI: str = os.getenv("MONGO_URI") or "mongodb://localhost:27017"

# Create a MongoDB client
mongo_client = AsyncIOMotorClient(MONGO_URI)

# Access a specific database and collection
workflows_db = mongo_client.cluster0
collection = workflows_db.workflows

app = Sanic("PrediKit")
CORS(app)
app.ctx.cache = dict()

app.config.REQUEST_TIMEOUT = sys.maxsize
app.config.RESPONSE_TIMEOUT = sys.maxsize


class SSEFilter(logging.Filter):
    def filter(self, record):
        return not (record.request.endswith("/sse") and record.status == 200)  # type: ignore


access_logger.addFilter(SSEFilter())


@app.route("/workflows/<workflow_id:str>/nodes")
async def nodes(_):
    """Gets a list of all nodes as well as the node information"""
    registry = NodeFactory.get_registry()
    logger.debug(category_order)

    # sort nodes in category order
    sorted_registry = sorted(
        registry.items(),
        key=lambda x: category_order.index(
            NodeFactory.create_node(x[0]).get_category()
        ),
    )
    node_list: list[Any] = []
    for schema_id, _node_class in sorted_registry:
        node_object = NodeFactory.create_node(schema_id)
        node_dict: dict[str, Any] = {
            "schemaId": schema_id,
            "name": node_object.get_name(),
            "category": node_object.get_category(),
            "inputs": [
                x.toDict()
                for x in node_object.get_inputs(with_implicit_ids=True)
            ],
            "outputs": [
                x.toDict()
                for x in node_object.get_outputs(with_implicit_ids=True)
            ],
            "description": node_object.get_description(),
            "icon": node_object.get_icon(),
            "subcategory": node_object.get_sub_category(),
            "nodeType": node_object.get_type(),
            "hasSideEffects": node_object.get_has_side_effects(),
            "seeAlso": node_object.get_see_also(),
            "kind": node_object.get_kind(),
            "deprecated": node_object.get_deprecated(),
            "features": node_object.get_features(),
        }
        if node_object.get_type() == "iterator":
            node_dict["defaultNodes"] = node_object.get_default_nodes()  # type: ignore
        node_list.append(node_dict)
    return json(node_list)


@app.route("/workflows/<workflow_id:str>/run", methods=["POST"])
async def run(request: Request, workflow_id: str):
    """Runs the provided nodes"""
    # headers = {"Cache-Control": "no-cache"}
    # await request.respond(response="Run request accepted", status=201, headers=headers)
    queue = request.app.ctx.queue

    try:
        if workflow_id in request.app.ctx.active_executors:
            logger.debug("Resuming existing executor...")
            executor = request.ctx.active_executors.get(workflow_id)
            await executor.resume()
        else:
            logger.debug("Running new executor...")
            full_data = dict(request.json)
            logger.debug(full_data)

            nodes_list = full_data["data"]
            executor = Executor(
                nodes_list, app.loop, queue, app.ctx.cache.copy()
            )
            request.ctx.active_executors[workflow_id] = executor
            await executor.run()
        if not executor.paused:
            request.ctx.active_executors.pop(workflow_id, None)
        # gc.collect()
        await queue.put(
            {"event": "finish", "data": {"message": "Successfully ran nodes!"}}
        )
        return json({"message": "Successfully ran nodes!"}, status=201)
    except Exception as exception:
        logger.error(exception, exc_info=True)
        request.ctx.active_executors.pop(workflow_id, None)
        logger.error(traceback.format_exc())
        await queue.put(
            {
                "event": "execution-error",
                "data": {
                    "message": "Error running nodes!",
                    "exception": str(exception),
                },
            }
        )
        return json(
            {"message": "Error running nodes!", "exception": str(exception)},
            status=500,
        )


@app.route("/workflows/<workflow_id:str>/run/individual", methods=["POST"])
async def run_individual(request: Request, _):
    """Runs a single node"""
    try:
        full_data = dict(request.json)
        logger.debug(full_data)
        # Create node based on given category/name information
        node_instance = NodeFactory.create_node(full_data["schemaId"])
        # Run the node and pass in inputs as args
        run_func = functools.partial(node_instance.run, *full_data["inputs"])
        output = await app.loop.run_in_executor(None, run_func)
        # Cache the output of the node
        app.ctx.cache[full_data["id"]] = output
        extra_data = node_instance.get_extra_data()
        del node_instance, run_func
        return json({"success": True, "data": extra_data})
    except Exception as exception:
        logger.error(exception, exc_info=True)
        return json({"success": False, "error": str(exception)})


@app.get("/workflows/<workflow_id:str>/sse")  # Server-Sent Events
async def sse(request: Request):
    headers = {"Cache-Control": "no-cache"}
    response = await request.respond(
        headers=headers, content_type="text/event-stream"
    )
    while True:
        message = await request.app.ctx.queue.get()
        if not message:
            break
        if response is not None:
            await response.send(f"event: {message['event']}\n")
            await response.send(f"data: {stringify(message['data'])}\n\n")


@app.after_server_start
async def setup_server(sanic_app: Sanic, _):
    sanic_app.ctx.queue = asyncio.Queue()
    sanic_app.ctx.active_executors = ConcurrencySafeDict()


@app.route("/workflows/<workflow_id:str>/pause", methods=["POST"])
async def pause(request, workflow_id) -> Any:
    """Pauses the current execution"""
    try:
        if workflow_id in request.app.ctx.active_executors:
            logger.debug("Executor found. Attempting to pause...")
            await request.ctx.active_executors[workflow_id].pause()
            return json(
                {"message": "Successfully paused execution!"}, status=201
            )
        logger.debug("No executor to pause")
        return json({"message": "No executor to pause!"}, status=201)
    except Exception as exception:
        logger.log(2, exception, exc_info=True)
        return json(
            {
                "message": "Error pausing execution!",
                "exception": str(exception),
            },
            status=500,
        )


@app.route("/workflows/<workflow_id:str>/kill", methods=["POST"])
async def kill(request: Request, workflow_id: str):
    """Kills the current execution"""
    try:
        if workflow_id in request.ctx.active_executors:
            logger.debug("Executor found. Attempting to kill...")
            await request.ctx.active_executors[workflow_id].kill()
            request.ctx.active_executors.pop(workflow_id, None)
            return json(
                {"message": "Successfully killed execution!"}, status=201
            )
        logger.debug("No executor to kill")
        return json({"message": "No executor to kill!"}, status=201)
    except Exception as exception:
        logger.log(2, exception, exc_info=True)
        return json(
            {
                "message": "Error killing execution!",
                "exception": str(exception),
            },
            status=500,
        )


@app.route("/workflows", methods=["POST"])
async def create_workflow(request: Request):
    """Creates a new workflow in the database"""
    try:
        data = request.json
        result = await collection.insert_one(data)
        return json(
            {
                "message": "Successfully created workflow!",
                "id": str(result.inserted_id),
            },
            status=201,
        )
    except Exception as exception:
        logger.error(exception, exc_info=True)
        return json(
            {
                "message": "Error creating workflow!",
                "exception": str(exception),
            },
            status=500,
        )
    finally:
        del data, result


@app.route("/workflows", methods=["GET"])
async def get_all_workflows(request: Request):
    """Gets all workflows from the database"""
    try:
        workflows = await collection.find().to_list(length=None)
        return json(workflows)
    except Exception as exception:
        logger.error(exception, exc_info=True)
        return json(
            {
                "message": "Error getting workflows!",
                "exception": str(exception),
            },
            status=500,
        )
    finally:
        del workflows


@app.route("/workflows/<workflow_id:str>", methods=["GET"])
async def get_workflow(request: Request, workflow_id: str):
    """Gets a specific workflow from the database"""
    try:
        workflow = await collection.find_one({"_id": workflow_id})
        return json(workflow)
    except Exception as exception:
        logger.error(exception, exc_info=True)
        return json(
            {
                "message": "Error getting workflow!",
                "exception": str(exception),
            },
            status=500,
        )
    finally:
        del workflow


@app.route("/workflows/<workflow_id:str>", methods=["DELETE"])
async def delete_workflow(request: Request, workflow_id: str):
    """Deletes a specific workflow from the database"""
    try:
        result = await collection.delete_one({"_id": workflow_id})
        return json(
            {
                "message": "Successfully deleted workflow!",
                "deletedCount": result.deleted_count,
            },
            status=201,
        )
    except Exception as exception:
        logger.error(exception, exc_info=True)
        return json(
            {
                "message": "Error deleting workflow!",
                "exception": str(exception),
            },
            status=500,
        )
    finally:
        del result


@app.route("/workflows/<workflow_id:str>", methods=["PUT"])
async def update_workflow(request: Request, workflow_id: str):
    """Updates a specific workflow in the database"""
    try:
        data = request.json
        result = await collection.replace_one({"_id": workflow_id}, data)
        return json(
            {
                "message": "Successfully updated workflow!",
                "modifiedCount": result.modified_count,
            },
            status=201,
        )
    except Exception as exception:
        logger.error(exception, exc_info=True)
        return json(
            {
                "message": "Error updating workflow!",
                "exception": str(exception),
            },
            status=500,
        )
    finally:
        del data, result


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
