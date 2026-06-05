from contextlib import contextmanager

@contextmanager
def my_context():

    print("hello")

    yield

    print("goodbye")