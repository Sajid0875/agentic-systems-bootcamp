def inifnite_sequence():
    num=0 
    while True:
        yield num
        num+=1

def square(sequence):
    for num in sequence :
        yield num**2

def pick_even(sequence):
    for num in sequence:
        if num%2==0:
            yield num 

numbers=inifnite_sequence()
squared=square(numbers)
even=pick_even(squared)

for _ in range(10):
    print(next(even))