from colorama import Fore, Back
from pprint import pp

import time
import threading

lock = threading.Lock()
barrier = threading.Barrier(2)

pipe = []


# def funct0(lock: threading.Lock):
def funct0():
    print("funct0 reached barrier")
    barrier.wait()
    global lock
    print("funct0 start")
    for index in range(5):
        print("funct0 acquiring lock")
        lock.acquire()
        print(f"funct0 pause after index {index}")
        # time.sleep(1)
        print("funct0 releasing lock")
        lock.release()
        print("funct0 going to sleep")
        time.sleep(1)
        print("funct0 woke up")
    print("funct0 ends")


# def funct1(lock: threading.Lock):
def funct1():
    print("funct1: start")
    # print("funct1: reached barrier")
    # barrier.wait()
    for index in range(5):
        print("funct1: acquiring lock")
        print(f"funct1: lock is locked?: {lock.locked()}")
        start = time.perf_counter()
        lock.acquire()
        end = time.perf_counter()
        print(
            f"{Back.RED}funct1:{Back.GREEN} acquired lock in: {end - start} seconds{Back.RESET}"
        )
        print(
            f"{Back.RED}funct1:{Back.GREEN} putting index {index} in pipe{Back.RESET}"
        )
        pipe.append(f"funct1: {index}")
        # print("funct1: started processing cpu bound task")
        # start = time.perf_counter()
        # delay = 1
        # for idx in range(int(5500000 * delay)):
        #     print("", end="")
        # end = time.perf_counter()
        # print(
        #     f"{Back.RED}funct1:{Back.GREEN} finished processing cpu bound task: {end - start} seconds{Back.RESET}"
        # )
        # print("funct1: going to sleep")
        time.sleep(1)
        # print("funct1: woke up")
        print(f"{Back.RED}funct1:{Back.GREEN} releasing lock{Back.RESET}")
        lock.release()
        # print("funct1: going to sleep")
        time.sleep(0.1)
        # print("funct1: woke up")
    print("funct1: ends")


if __name__ == "__main__":
    """
    acquiring a lock doesn't mean that execution of other threads
    stops, it just means that any attempt to acquire this lock from
    other threads will block execution of that thread, if the thread
    has not reached this acquire statement, it's execution will
    continue
    """
    print("main: start")
    # lock.acquire()

    # lock = threading.Lock()
    # thread0 = threading.Thread(target=funct0, name="thread0", args=(lock,))
    # thread0 = threading.Thread(target=funct0, name="thread0")
    # thread0.start()
    # print("back in main")
    # thread1 = threading.Thread(target=funct1, name="thread1", args=(lock,))
    thread1 = threading.Thread(target=funct1, name="thread1")
    thread1.start()
    print("back in main")
    # print("main: reached barrier")
    # barrier.wait()
    # while thread0.is_alive() and thread1.is_alive():
    #     print("back in main")
    #     time.sleep(3)
    # thread0.join()
    for index in range(5):
        print("main: acquiring lock")
        print(f"main: lock is locked?: {lock.locked()}")
        start = time.perf_counter()
        lock.acquire()
        end = time.perf_counter()
        print(
            f"{Back.YELLOW}main:{Back.GREEN} acquired lock in: {end - start} seconds{Back.RESET}"
        )
        print(
            f"{Back.YELLOW}main:{Back.GREEN} putting index {index} in pipe{Back.RESET}"
        )
        pipe.append(f"main: {index}")
        # print("main: started processing cpu bound task")
        # start = time.perf_counter()
        # delay = 1
        # for idx in range(int(5500000 * delay)):
        #     print("", end="")
        # end = time.perf_counter()
        # print(
        #     f"{Back.YELLOW}main:{Back.GREEN} finished processing cpu bound task: {end - start} seconds{Back.RESET}"
        # )
        # print("main: going to sleep")
        time.sleep(1)
        # print("main: woke up")
        print(f"{Back.YELLOW}main:{Back.GREEN} releasing lock{Back.RESET}")
        lock.release()
        """
        here when we release it, we should give opportunity for
        other threads to acquire the lock, coz the loop in
        current thread can start it's next iteration super quickly
        and the other thread doesn't get a chance to acquire it,
        this is on the whims and fancies of os, is time.sleep that
        opportunity?, even if we give the opportunity, it's on the os
        to take it or not
        """
        # print("main: going to sleep")
        time.sleep(0.1)
        """
        time sleep explicity triggers suspension of the current thread
        """
        # print("main: woke up")
    thread1.join()
    print("main: ends")
    pp(pipe)
