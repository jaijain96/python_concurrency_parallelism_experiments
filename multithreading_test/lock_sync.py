import threading
import time
from pprint import pp

from colorama import Back


def funct(lock: threading.Lock, pipe: list):
    print(f"{Back.CYAN}thread: begin{Back.RESET}")
    print(
        f"{Back.CYAN}thread: going to sleep for 0.05 sec to make sure there is no race condition between this thread and main, this is to make sure that main is ahead in its execution, ensuring that main is the producer and this thread is the consumer{Back.RESET}"
    )
    begin = time.perf_counter()
    time.sleep(0.05)  # release execution
    end = time.perf_counter()
    print(f"{Back.CYAN}thread: woke up after {end - begin} secs{Back.RESET}")
    for index in range(5):
        print(
            f"{Back.CYAN}thread: going to sleep for 0.1 sec to make sure there is no race condition between this thread and main, this will allow main to acquire lock and push something in pipe{Back.RESET}"
        )
        begin = time.perf_counter()
        time.sleep(0.1)  # release execution
        end = time.perf_counter()
        print(f"{Back.CYAN}thread: woke up after {end - begin} secs{Back.RESET}")
        # print(f"{Back.CYAN}thread: attempting to acquire lock{Back.RESET}")
        # begin = time.perf_counter()
        # lock.acquire()
        # end = time.perf_counter()
        # print(f"{Back.CYAN}thread: acquired lock in: {end - begin} seconds{Back.RESET}")
        print(f"{Back.GREEN}thread: popping {pipe.pop()} from pipe{Back.RESET}")
        # print(f"{Back.CYAN}thread: releasing lock{Back.RESET}")
        # lock.release()
    print(f"{Back.CYAN}thread: ends{Back.RESET}")


if __name__ == "__main__":
    print(f"{Back.YELLOW}main: begin{Back.RESET}")
    lock = threading.Lock()
    """
    acquiring a lock doesn't mean that execution of other threads
    stops, it just means that any attempt to acquire this lock from
    other threads will block execution of that thread, if the thread
    has not reached this acquire statement, it's execution will
    continue
    """
    pipe = []
    thread = threading.Thread(target=funct, name="thread", args=(lock, pipe))
    thread.start()
    """
    note that when we are begining another thread and we haven't acquired a
    lock in the current thread, we are essentially inducing a race condition 
    between the current thread and the new thread(s) to acquire the lock;
    to prevent this, we deliberately suspend the execution of the other thread
    using time.sleep() so that main thread can proceed to acquire the lock and
    push in some data into the communication pipe (acting as queue)
    """
    print(f"{Back.YELLOW}back in main{Back.RESET}")
    for index in range(5):
        print(
            f"{Back.YELLOW}main: going to sleep for 0.1 sec to make sure there is no race condition between main and any other thread, this will allow main to acquire lock and push something in pipe{Back.RESET}"
        )
        begin = time.perf_counter()
        time.sleep(0.1)  # release execution
        end = time.perf_counter()
        print(f"{Back.YELLOW}main: woke up after {end - begin} secs{Back.RESET}")
        # print(f"{Back.YELLOW}main: attempting to acquire lock{Back.RESET}")
        # begin = time.perf_counter()
        # lock.acquire()
        # end = time.perf_counter()
        # print(f"{Back.YELLOW}main: acquired lock in: {end - begin} seconds{Back.RESET}")
        print(f"{Back.GREEN}main: putting index {index} in pipe{Back.RESET}")
        pipe.append(index)
        """
        can we do without the above time.sleep(1)?
        consider what happens if we don't suspend the execution of the
        current thread, the current thread acquires the lock from a
        previous thread which would have given up control of the lock
        using lock.release()
        if we don't have time.sleep(1), the current thread acquires
        the thread and releases very quickly, this would cause a race
        condition between the current thread and other thread(s) waiting to
        acquire the lock
        """
        # print(f"{Back.YELLOW}main: releasing lock{Back.RESET}")
        # lock.release()  # release lock
        """
        can we do without the above time.sleep(0.5)?
        when we release the lock, we should give opportunity for
        other threads to acquire the lock, coz the loop in
        current thread can begin it's next iteration super quickly
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
