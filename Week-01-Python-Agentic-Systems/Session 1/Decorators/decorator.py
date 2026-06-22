def decorator(func):

    def wrapper():
        print("Starting")
        func()
        print("Finished")

    return wrapper


@decorator
def greet():  # we have function argument issue here, greet is not. accepting any arguments

    print("Hello")

#greet = decorator(greet)

greet()

