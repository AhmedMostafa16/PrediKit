import msgpack
import logging
import zmq
import asyncio
import zmq.asyncio
from process_data import process_data
import logging
from process_data import process_data
import multiprocessing


async def worker(queue_in, queue_out):
    while True:
        data = await queue_in.get()
        response: str = ""
        if data == "Ping":
            response = "Pong"
        else:
            response = await process_data(data)
        await queue_out.put(response)


async def server(address):
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.REP)
    socket.bind(address)

    # Get the number of CPU cores
    pool_size = multiprocessing.cpu_count()
    logging.info(f"Started {pool_size} processes")

    # Create asyncio queues for communication between worker and server
    queue_in = asyncio.Queue()
    queue_out = asyncio.Queue()
    # logging.info("Created asyncio queues")

    # Start worker processes
    workers = [
        asyncio.create_task(worker(queue_in, queue_out))
        for _ in range(pool_size)
    ]
    logging.info("Started worker tasks")

    # Define a coroutine to monitor the number of active asyncio tasks and processes
    # and write the information to a log file
    # This is a simple but useful way for debugging and monitoring the server
    async def monitor_tasks():
        log_file = "/tmp/monitor.log"
        previous_task_count = 0
        previous_process_count = 0
        previous_queue_in_size = 0
        previous_queue_out_size = 0

        while True:
            # Get the current number of active asyncio tasks and processes
            task_count = len(asyncio.all_tasks())
            process_count = len(multiprocessing.active_children())
            queue_in_size = queue_in.qsize()
            queue_out_size = queue_out.qsize()

            # Check if there is a change in the monitoring information
            if (
                task_count != previous_task_count
                or process_count != previous_process_count
                or queue_in_size != previous_queue_in_size
                or queue_out_size != previous_queue_out_size
            ):
                # Write the monitoring information to the log file
                with open(log_file, "a") as f:
                    f.write(
                        f"Active asyncio tasks: {task_count}, Active processes: {process_count}\n"
                    )
                    f.write(
                        f"Queue in size: {queue_in_size}, Queue out size: {queue_out_size}\n"
                    )
                    f.write("\n")

                # Update the previous values
                previous_task_count = task_count
                previous_process_count = process_count
                previous_queue_in_size = queue_in_size
                previous_queue_out_size = queue_out_size

            await asyncio.sleep(0.5)

    # monitor_task = asyncio.create_task(monitor_tasks())

    try:
        while True:
            # Receive request from client
            request = await socket.recv()

            # Deserialize request
            decoded = msgpack.unpackb(request, raw=False)

            # Put the request into the queue for processing
            await queue_in.put(decoded)

            # Get the result from the queue and send it to the client
            response: str = await queue_out.get()
            await socket.send_string(response)

    except asyncio.CancelledError:
        logging.error("Asyncio Cancelled")
        pass
    except Exception as e:
        logging.error(f"Exception: {e}")
        pass
    finally:
        # Clean up
        for worker_task in workers:
            worker_task.cancel()
        # monitor_task.cancel()
        await asyncio.gather(*workers, return_exceptions=True)


if __name__ == "__main__":
    server_address = "tcp://127.0.0.1:5555"
    logging.basicConfig(level=logging.INFO)
    asyncio.run(server(server_address))
