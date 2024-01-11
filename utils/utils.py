from multiprocessing import Process


def func1():
    print("func1: starting")
    for i in range(10000000):
        pass

    print("func1: finishing")


def func2():
    print("func2: starting")
    for i in range(10000000):
        pass

    print("func2: finishing")

def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

runInParallel(func1, func2)


