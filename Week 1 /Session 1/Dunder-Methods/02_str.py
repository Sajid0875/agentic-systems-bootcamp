class student:
    def __init__(self, age):
        self.age = age
    def __str__(self):
        return str(self.age)
s=student(20)
print(s)