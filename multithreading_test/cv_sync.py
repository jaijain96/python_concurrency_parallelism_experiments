import threading
import time
from pprint import pp

from colorama import Back


def funct(cv: threading.Condition, lock: threading.Lock, pipe: list):
    # thread is consumer, main adds to the pipe and thread
    # consumes it
    print(f"{Back.CYAN}thread: start{Back.RESET}")
    print(f"{Back.CYAN}thread: acquiring lock{Back.RESET}")
    if lock.locked():
        print(f"{Back.RED}thread: waiting for lock to be released...{Back.RESET}")
    start = time.perf_counter()
    cv.acquire()
    end = time.perf_counter()
    print(f"{Back.CYAN}thread: acquired lock in: {end - start} seconds{Back.RESET}")
    for index in range(5):
        while not len(pipe):
            print(
                f"{Back.CYAN}thread: going to release lock and wait to be notified if anything in pipe...{Back.RESET}"
            )
            start = time.perf_counter()
            cv.wait()  # releases the lock, blocks, waits to
            # be notified, when notified, will attempt to
            # acquire lock?
            # if lock available -> acquire and continue
            # if lock not available? -> error
        end = time.perf_counter()
        print(
            f"{Back.CYAN}thread: waited for and acquired lock in: {end - start} seconds{Back.RESET}"
        )
        # print("thread: acquiring lock")
        # if lock.locked():
        #     print(f"{Back.RED}thread: waiting for lock to be released...{Back.RESET}")
        # lock.acquire()
        # print(f"{Back.CYAN}thread: putting index {index} in pipe{Back.RESET}")
        # pipe.append(f"thread: {index}")
        print(f"{Back.CYAN}thread: received: {pipe.pop()} from pipe{Back.RESET}")
        # time.sleep(1)
        # producer should have the lock and be waiting at this point
        cv.notify_all()  # doesn't give up control, need to release lock
        print(f"{Back.CYAN}thread: notified that it's done popping{Back.RESET}")
        # print(f"{Back.CYAN}thread: releasing lock{Back.RESET}")
        # lock.release()
        # cv.release()  # release won't stop execution of this thread,
        # we need to make it wait as well? most likely yes coz this
        # will rush to acquire the lock,
        # wait() will reacquire the lock, no need to explicitly
        # reacquire
        # time.sleep(0.5)
        # time.sleep(1)
    print(f"{Back.CYAN}thread: ends{Back.RESET}")


if __name__ == "__main__":
    # in lock_sync.py, manipulate to prevent race condition in start
    # so deterministic producer and consumer?
    print(f"{Back.YELLOW}main: start{Back.RESET}")
    lock = threading.Lock()
    cv = threading.Condition(lock=lock)

    # main is producer, it acquires the lock first?
    # cv.acquire()
    # print(ff"{Back.YELLOW}main: lock is locked?: {lock.locked()}")
    """
    acquiring a lock doesn't mean that execution of other threads
    stops, it just means that any attempt to acquire this lock from
    other threads will block execution of that thread, if the thread
    has not reached this acquire statement, it's execution will
    continue
    """
    pipe = []
    thread = threading.Thread(target=funct, name="thread", args=(cv, lock, pipe))
    thread.start()
    """
    note that when we are starting another thread and we haven't
    acquired a lock in the current thread, we are essentially inducing
    a race condition between the current thread and the new thread(s)
    to acquire the lock
    """
    print(f"{Back.YELLOW}main: back in main{Back.RESET}")
    print(
        f"{Back.YELLOW}main: going to sleep to allow consumer to be ready to process incoming messages{Back.RESET}"
    )
    time.sleep(0.5)  # let the consumer acquire lock and
    # reach wait, where it releases the lock
    print(f"{Back.YELLOW}main: woke up{Back.RESET}")
    print(f"{Back.YELLOW}main: acquiring lock{Back.RESET}")
    if lock.locked():
        print(f"{Back.RED}main: waiting for lock to be released...{Back.RESET}")
    start = time.perf_counter()
    cv.acquire()
    end = time.perf_counter()
    print(f"{Back.YELLOW}main: acquired lock in: {end - start} seconds{Back.RESET}")
    for index in range(5):
        print(f"{Back.YELLOW}main: putting index {index} in pipe{Back.RESET}")
        pipe.append(index)
        # cv.notify()
        cv.notify_all()
        print(f"{Back.YELLOW}main: notified that it's done pushing{Back.RESET}")
        # print(f"{Back.YELLOW}main: releasing lock{Back.RESET}")
        # cv.release()
        # time.sleep(1)  # let the consumer acquire the lock
        # using wait(), then proceed to pop and then release
        # the lock
        # or we release the lock ourself?
        if index == 4:
            print(f"{Back.YELLOW}main: going to release lock{Back.RESET}")
            start = time.perf_counter()
            cv.release()
            end = time.perf_counter()
            print(
                f"{Back.YELLOW}main: released lock in: {end - start} seconds{Back.RESET}"
            )
        else:
            while len(pipe):
                print(
                    f"{Back.YELLOW}main: going to release lock and wait to be notified when pipe is empty...{Back.RESET}"
                )
                start = time.perf_counter()
                cv.wait()
            end = time.perf_counter()
            print(
                f"{Back.YELLOW}main: waited for and acquired lock in: {end - start} seconds{Back.RESET}"
            )
        # print(f"{Back.YELLOW}main: putting index {index} in pipe{Back.RESET}")
        # pipe.append(index)
        # cv.notify()
        # time.sleep(1)
        """
        can we do without the above time.sleep(1)?
        consider what happens if we don't suspend the execution of the
        current thread, the current thread acquires the lock from a
        previous thread which would have given up control of the lock
        using lock.release()
        if we don't have time.sleep(1), the current thread acquires
        the thread and releases very quickly, this would cause a race
        condition between the current thread and the previous thread
        or any other thread waiting to acquire the lock
        """
        # print(f"{Back.YELLOW}main: releasing lock{Back.RESET}")
        # cv.release()
        # lock.release()
        # time.sleep(0.5)
        """
        can we do without the above time.sleep(0.5)?
        when we release the lock, we should give opportunity for
        other threads to acquire the lock, coz the loop in
        current thread can start it's next iteration super quickly
        and the other threads don't get a chance to acquire it,
        it is on the whims of the os to suspend control of this thread
        and let the other threads run a few statement so they can
        attempt to acquire the lock, instead, we suspend the current
        thread explicitly;
        time.sleep explicity triggers suspension of the current
        thread for a specified amount of time, this gives other
        threads a chance to execute some of their statements and
        reach the acquire statement and attempt to acquire the lock;
        in case we don't do this, it is possible that the current
        thread releases the lock, releasing the lock doesn't mean
        giving up execution, so it continues execution and again
        acquires the lock;
        this is again an example of race condition, here we only 
        have one thread that will resume execution when the current
        thread is suspended using time.sleep, if there are more than 
        one thread waiting to acquire the lock, we have a race among
        the threads to acquire the lock, since it's not deterministic
        which thread gets the lock (depends on the os), this behaviour
        is not desirable
        """
    thread.join()
    print(f"{Back.YELLOW}main: ends{Back.RESET}")
    """
    here we are using locks as a synchronization mechanism but
    we also rely on time.sleep() to prevent race conditions, are there
    any other mechanisms to prevent these race conditions
    """
