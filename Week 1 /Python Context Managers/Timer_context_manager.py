import contextlib
import time 

@contextlib.contextmanager

def timer():
    start_time=time.time()
    yield
    end_time=time.time()
    print(f'Elapsed time: {end_time-start_time:.4f} seconds')

with timer():
    print('This should take approximately 0.25 seconds')
    time.sleep(0.25)