import asyncio
import time
import functools
import concurrent


async def awaitable_coroutine(iter, delay):
    print(f"this is from async method: {iter}")
    begin = time.perf_counter()
    await asyncio.sleep(delay)
    end = time.perf_counter()
    print(f"async method: {iter} done in {end - begin}")


async def spawner_coroutine_with_gather():
    num_tasks = 3
    tasks = []
    for iter in range(num_tasks):
        tasks.append(awaitable_coroutine(iter, num_tasks - iter))
    await asyncio.gather(*tasks)


async def spawner_coroutine_no_gather():
    num_tasks = 3
    tasks = []
    for iter in range(num_tasks):
        tasks.append(asyncio.create_task(awaitable_coroutine(iter, num_tasks - iter)))
    for task in tasks:
        await task


def non_awaitable_method(iter, delay):
    """blocking_method io"""
    print(f"this is from sync method io: {iter}")
    begin = time.perf_counter()
    time.sleep(delay)
    end = time.perf_counter()
    print(f"sync method io: {iter} done in {end - begin}")


def non_awaitable_method_cpu(iter, delay):
    """blocking cpu"""
    print(f"this is from sync method cpu: {iter}")
    begin = time.perf_counter()
    for idx in range(5500000 * delay):
        print("", end="")  # print method is important here, can't simply use pass
    end = time.perf_counter()
    print(f"sync method cpu: {iter} done in {end - begin}")


async def spawner_method_template():
    # # note that directly calling await will run the coroutine but will block execution
    # await asyncio.to_thread(non_awaitable_method(1, 2))
    # await asyncio.to_thread(non_awaitable_method(2, 1))

    # # this will throw runtime error
    # task0 = asyncio.to_thread(non_awaitable_method(1, 2))
    # task1 = asyncio.to_thread(non_awaitable_method(2, 1))
    # await task0
    # await task1

    # # to run coroutines concurrently, create tasks and then call await on them
    # task0 = asyncio.create_task(asyncio.to_thread(non_awaitable_method(0, 2)))
    # task1 = asyncio.create_task(asyncio.to_thread(non_awaitable_method(1, 2)))
    # await task0
    # await task1

    # # this could also be in a loop like this
    # tasks = []
    # for idx in range(2):
    #     task = asyncio.create_task(asyncio.to_thread(non_awaitable_method(0, 2)))
    #     # can't call await task here coz that will block since there won't be any other coroutines in the current loop
    #     tasks.append(task)
    # for task in tasks:
    #     await task

    # asyncio.gather can be used as well from within a running loop as it
    # doesn't create a new loop and schedules coroutines on the current loop,
    # this alleviates the need to create tasks manually
    # coros = []
    # for idx in range(2):
    #     coro = asyncio.to_thread(non_awaitable_method(0, 2))
    #     coros.append(coro)
    # await asyncio.gather(*coros)

    # await asyncio.gather(
    #     asyncio.to_thread(functools.partial(non_awaitable_method, 1, 2)),
    #     asyncio.to_thread(functools.partial(non_awaitable_method, 2, 1)),
    # )
    pass


async def spawner_method(io=False, cpu=False, cpu_multi=False):
    if io:
        tasks = []
        for idx in range(5):
            task = asyncio.create_task(
                asyncio.to_thread(functools.partial(non_awaitable_method, idx, 5))
            )
            tasks.append(task)

        for task in tasks:
            await task

    if cpu:
        tasks = []
        for idx in range(5):
            task = asyncio.create_task(
                asyncio.to_thread(functools.partial(non_awaitable_method_cpu, idx, 5))
            )
            tasks.append(task)

        for task in tasks:
            await task

    if cpu_multi:
        loop = asyncio.get_running_loop()
        with concurrent.futures.ProcessPoolExecutor() as pool:
            for idx in range(5):
                loop.run_in_executor(
                    pool, functools.partial(non_awaitable_method_cpu, idx, 5)
                )


# def sync_spawner():
#     start = time.perf_counter()

#     # asyncio.run(spawner_coroutine_with_gather())
#     # asyncio.run(spawner_coroutine_no_gather())
#     asyncio.run(spawner_method())

#     end = time.perf_counter()
#     print(f"total time: {end - start}")


if __name__ == "__main__":
    # asyncio.run(spawner_coroutine_with_gather())
    # asyncio.run(spawner_coroutine_no_gather())
    io = 0
    cpu = 0
    cpu_multi = 0
    begin = time.perf_counter()
    asyncio.run(spawner_method(io=io), debug=True)
    end = time.perf_counter()
    print(f"total time taken io: {end - begin}")
    begin = time.perf_counter()
    asyncio.run(spawner_method(cpu=cpu), debug=True)
    end = time.perf_counter()
    print(f"total time taken cpu: {end - begin}")
    begin = time.perf_counter()
    asyncio.run(spawner_method(cpu_multi=cpu_multi), debug=True)
    end = time.perf_counter()
    print(f"total time taken cpu multi: {end - begin}")
