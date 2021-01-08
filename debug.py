import sys


def is_debug_active():
    # https://stackoverflow.com/questions/38634988/check-if-program-runs-in-debug-mode
    gettrace = getattr(sys, 'gettrace', None)
    if gettrace is not None and gettrace():
        return True
    return False

    # if gettrace is None:
    #     print('No sys.gettrace')
    # elif gettrace():
    #     print('Hmm, Big Debugger is watching me')
    # else:
    #     print("Let's do something interesting")
    #     print(1 / 0)
