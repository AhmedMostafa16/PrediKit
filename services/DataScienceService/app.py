import gc
import logging
import multiprocessing
import sys
import threading
import msgpack
import zmq
from process_data import process_data


NUMBER_OF_WORKERS: int = multiprocessing.cpu_count()


def tprint(msg) -> None:
    """like print(), but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


def worker_task(id) -> None:
    """Worker task, using a REQ socket to do load-balancing."""
    socket = zmq.Context().instance().socket(zmq.REQ)
    socket.identity = "W-{}".format(id).encode("ascii")
    socket.connect("ipc://backend.ipc")
    # logging.info(f"Worker-{id} is ready")

    # Tell broker that the worker is ready for work
    socket.send(b"READY")
    try:
        while True:
            address, empty, request = (
                socket.recv_multipart()
            )  # Receive a request from the broker
            message = msgpack.unpackb(request)  # Decode the message
            # tprint("Received request: %s" % message)

            # Do some 'work'
            if message == b"Ping":
                response = b"Pong"
            else:
                response = process_data(message)
                # response = b"Ok"

            # tprint("{}: {}".format(socket.identity.decode("ascii"), message))
            socket.send_multipart(
                [address, b"", response]
            )  # Send the reply back to the broker
    except Exception as e:
        logging.error(e)
        socket.close()


def broker() -> None:
    """Load balancer main loop."""
    # Prepare context and sockets
    context = zmq.Context().instance()
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://*:5555")
    backend = context.socket(zmq.ROUTER)
    backend.bind("ipc://backend.ipc")

    # logging.info("Load balancer is ready")

    # Initialize main loop state
    backend_ready = False
    workers: list[bytes] = []
    poller = zmq.Poller()

    # Only poll for requests from backend until workers are available
    poller.register(backend, zmq.POLLIN)
    # logging.info("Polling for requests from backend")

    while True:
        try:
            sockets = dict(poller.poll())
        except Exception as e:
            logging.error(e)
            break

        if backend in sockets:
            # logging.info("Received request from backend")
            # Handle worker activity on the backend
            request = backend.recv_multipart()
            worker, _, client = request[:3]
            workers.append(worker)
            if workers and not backend_ready:
                # Poll for clients now that a worker is available and backend was not ready
                poller.register(frontend, zmq.POLLIN)
                backend_ready = True
            if client != b"READY" and len(request) > 3:
                # If client reply is not just a READY message, route it to the frontend
                _, reply = request[3:]
                frontend.send_multipart([client, reply])

        if frontend in sockets:
            # logging.info("Received request from frontend")
            # Get next client request, route to last-used worker
            client, request = frontend.recv_multipart()
            worker = workers.pop(0)  # Pop the first worker from the list
            backend.send_multipart(
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
    gc.collect()


def main():
    worker_processes: list = []
    try:
        # Start broker
        broker_thread = threading.Thread(
            target=broker, daemon=True, name="Broker"
        )
        logging.info("Started the server")
        broker_thread.start()

        # Start background tasks
        for i in range(NUMBER_OF_WORKERS):
            process = multiprocessing.Process(
                target=worker_task,
                args=(i,),
                daemon=True,
                name=f"P-{i}",
            )
            worker_processes.append(process)
            process.start()
        # logging.info(f"Started {NUMBER_OF_WORKERS} worker processes")

    except KeyboardInterrupt:
        logging.info("Interrupted")
    except Exception as e:
        logging.error(e)
    finally:
        # Clean up
        broker_thread.join()

        # Wait for the broker process to finish
        for process in worker_processes:
            process.join()

        # Terminate all the worker processes
        for process in multiprocessing.active_children():
            process.terminate()

        logging.info("Terminated all the worker processes")
        logging.info("Stopped the server")
        gc.collect(2)


if __name__ == "__main__":
    if __debug__:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    main()
