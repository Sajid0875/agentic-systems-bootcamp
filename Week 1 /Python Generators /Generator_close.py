def infinite_counter():
    count = 0
    try:
        while True:
            yield count
            count += 1
    except GeneratorExit:
        print("Generator closed!")

# Using the generator
counter = infinite_counter()

print(next(counter))  # Output: 0
print(next(counter))  # Output: 1
counter.close()       # Output: "Generator closed!"