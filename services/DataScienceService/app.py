import asyncio

import multiprocessing
import sys
import msgpack
import zmq.asyncio
from process_data import process_data


NUMBER_OF_WORKERS: int = multiprocessing.cpu_count() * 2  # Number of workers


def tprint(msg):
    """like print(), but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


async def worker_task(ident):
    """Worker task, using a REQ socket to do load-balancing."""
    socket = zmq.asyncio.Context().socket(zmq.REQ)
    socket.identity = "Worker-{}".format(ident).encode("ascii")
    socket.connect("ipc://backend.ipc")

    # Tell broker that the worker is ready for work
    await socket.send(b"READY")

    while True:
        address, empty, request = (
            await socket.recv_multipart()
        )  # Receive a request from the broker
        message = msgpack.unpackb(request)  # Decode the message
        # tprint("Received request: %s" % message)

        # Do some 'work'
        if message == b"Ping":
            response = b"Pong"
        else:
            response = await process_data(
                message
            )  # TODO: Get rid of Zombie processes
            # response = b"Ok"

        # tprint("{}: {}".format(socket.identity.decode("ascii"), message))
        await socket.send_multipart(
            [address, b"", response]
        )  # Send the reply back to the broker


async def main():
    """Load balancer main loop."""
    # Prepare context and sockets
    context = zmq.asyncio.Context().instance()
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://*:5555")
    backend = context.socket(zmq.ROUTER)
    backend.bind("ipc://backend.ipc")

    # Start background tasks
    worker_processes: list[multiprocessing.Process] = []
    for i in range(NUMBER_OF_WORKERS):
        process = multiprocessing.Process(
            target=asyncio.run,
            args=(worker_task(i),),
            daemon=True,
            name=f"Worker-{i}",
        )
        worker_processes.append(process)
        process.start()

    # Initialize main loop state
    backend_ready = False
    workers: list[bytes] = []
    poller = zmq.asyncio.Poller()

    # Only poll for requests from backend until workers are available
    poller.register(backend, zmq.POLLIN)

    while True:
        sockets = dict(await poller.poll())

        if backend in sockets:
            # Handle worker activity on the backend
            request = await backend.recv_multipart()
            worker, _, client = request[:3]
            workers.append(worker)
            if workers and not backend_ready:
                # Poll for clients now that a worker is available and backend was not ready
                poller.register(frontend, zmq.POLLIN)
                backend_ready = True
            if client != b"READY" and len(request) > 3:
                # If client reply is not just a READY message, route it to the frontend
                _, reply = request[3:]
                await frontend.send_multipart([client, reply])

        if frontend in sockets:
            # Get next client request, route to last-used worker
            client, request = await frontend.recv_multipart()
            worker = workers.pop(0)  # Pop the first worker from the list
            await backend.send_multipart(
                [worker, b"", client, b"", request]
            )  # Send the client's message to the worker
            if not workers:
                # If no workers are available, unregister the frontend
                # Don't poll clients if no workers are available and set backend_ready flag to false
                poller.unregister(frontend)
                backend_ready = False

    # Clean up
    backend.close()
    frontend.close()
    context.term()
    for process in worker_processes:
        process.join()

    for process in multiprocessing.active_children():
        process.terminate()


if __name__ == "__main__":
    asyncio.run(main())
