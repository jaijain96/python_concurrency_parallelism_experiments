import asyncio
import time
import functools


async def awaitable_coroutine(delay):
    # async def awaitable_coroutine(iter, delay):
    print("this is from async method")
    # print(f"this is from async method: {iter}")
    start = time.perf_counter()
    await asyncio.sleep(delay)
    end = time.perf_counter()
    print(f"async method done in {end - start}")
    # print(f"async method: {iter} done in {end - start}")
    return {"async": delay}


async def crucible_inference(delay):
    return await awaitable_coroutine(delay)


def non_awaitable_method(delay):
    # def non_awaitable_method(iter, delay):
    """blocking io"""
    print("this is from sync method")
    # print(f"this is from sync method: {iter}")
    start = time.perf_counter()
    time.sleep(delay)  # batch call here
    end = time.perf_counter()
    print(f"sync method done in {end - start}")
    # print(f"sync method: {iter} done in {end - start}")
    return {"sync": delay}


async def dev_speed_inference(delay):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None, functools.partial(non_awaitable_method, delay)
    )
    # await asyncio.wait(
    #     fs={loop.run_in_executor(None, functools.partial(non_awaitable_method, delay))},
    #     return_when=asyncio.ALL_COMPLETED,
    # )
    # loop = asyncio.get_running_loop()
    # Run three of the blocking tasks concurrently. asyncio.wait will
    # automatically wrap these in Tasks. If you want explicit access
    # to the tasks themselves, use asyncio.ensure_future, or add a
    # "done, pending = asyncio.wait..." assignment
    # result = await asyncio.wait(
    #     fs={
    #         # Returns after delay=12 seconds
    #         loop.run_in_executor(executor_arg, blocking),

    #         loop.run_in_executor(executor_arg, blocking),

    #         loop.run_in_executor(executor_arg, blocking)
    #     },
    #     return_when=asyncio.ALL_COMPLETED
    # )
    # return result
    # await asyncio.to_thread(functools.partial(non_awaitable_method, 5))


async def fsc_inference():
    tasks = []
    tasks.append(crucible_inference(2))
    tasks.append(dev_speed_inference(5))
    return await asyncio.gather(*tasks)


async def test_spawner():
    start = time.perf_counter()

    # asyncio.run(spawner_method())
    # await spawner_method()
    responses = await fsc_inference()
    print(f"responses:\n{responses}")

    end = time.perf_counter()
    print(f"total time: {end - start}")
    assert 0 == 1
