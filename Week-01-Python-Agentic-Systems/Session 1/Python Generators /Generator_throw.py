def resilient_generator():
    try:
        for i in range(5):
            yield i
    except ValueError:
        yield "Error occurred!"

# Using the generator
gen = resilient_generator()
print(next(gen))  # Output: 0
print(next(gen))  # Output: 1
print(gen.throw(ValueError))  # Output: "Error occurred!" 