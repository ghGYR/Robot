import multiprocessing
import time


def worker(interval, name):
    n = 5
    while n > 0:
        print("The time is {0} from{1}".format(time.ctime(), name))
        time.sleep(interval)
        n -= 1
    print("I am over %s" % (name))


if __name__ == "__main__":
    p1 = multiprocessing.Process(target=worker, args=(3, "P1"))
    p2 = multiprocessing.Process(target=worker, args=(10, "P2"))
    p1.start()
    p2.start()
    print("p1.pid:", p1.pid)
    print("p1.name:", p1.name)
    print("p1.is_alive:", p1.is_alive())
    print("p2.pid:", p2.pid)
    print("p2.name:", p2.name)
    print("p2.is_alive:", p2.is_alive())
