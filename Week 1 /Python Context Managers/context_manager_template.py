from contextlib import contextmanager 
@contextmanager
def my_context():
    print("Setup")

    try:
        yield
    finally:
        print("Cleanup")

    
    with my_context():
        print("work")
        