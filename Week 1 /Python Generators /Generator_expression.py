squares_gen = (x**2 for x in range(5))

# Using the generator
for square in squares_gen:
    print(square)

# it is also called lazy evalvuation 