from time import time


def sw(fn):
    start = time()

    def a():
        return fn()

    print(f"{'{0:.6f}'.format(round((time() - start) * 1000.0, 2))} milliseconds")
    return a
