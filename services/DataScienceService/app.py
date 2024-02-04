import asyncio
import logging
import multiprocessing
import zmq.asyncio
from multiprocessing import Process, cpu_count
import msgpack

from process_data import process_data


def worker_function(
    worker_id: int,
    input_queue: multiprocessing.Queue,
    output_queue: multiprocessing.Queue,
):
    # logging.debug(f"Starting worker {worker_id}")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while True:
        task = input_queue.get()
        # logging.debug(f"Worker {worker_id} received task {task}")
        if task is None:
            break
        # Process the task
        if task == "Ping":
            result = "Pong"
        else:
            result: str = loop.run_until_complete(process_data(task))
        output_queue.put(result)
        # logging.debug(f"Worker {worker_id} sent result {result}")
    # logging.debug(f"Worker {worker_id} finished")


async def main():
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5555")

    num_workers = cpu_count() if cpu_count() > 4 else 4
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    # Start worker tasks concurrently
    workers = [
        Process(
            target=worker_function,
            args=(i, input_queue, output_queue),
        )
        for i in range(num_workers)
    ]

    for worker in workers:
        worker.start()

    try:
        while True:
            # Receive request
            request = await socket.recv()
            message = msgpack.unpackb(request, raw=False)
            # logging.debug(f"Received request: {request}")

            # Distribute tasks among workers
            input_queue.put(message)
            # logging.debug(f"Sent task {message} to worker")

            # Collect results from workers
            result = output_queue.get()
            # logging.debug(f"Received result from worker: {result}")

            # Send response
            response = result
            await socket.send_string(response)
            # logging.debug(f"Sent response to client: {response}")

    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        # Send stop signal to workers
        for _ in range(num_workers):
            input_queue.put(None)

        # Wait for workers to finish
        for worker in workers:
            worker.join()
        socket.close()
        context.term()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
