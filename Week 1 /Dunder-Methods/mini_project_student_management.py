class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name} ({self.age})"

    def __repr__(self):
        return f"Student('{self.name}', {self.age})"

    def __eq__(self, other):
        return self.name == other.name and self.age == other.age


s1 = Student("Ali", 21)
s2 = Student("Ali", 21)
s3 = Student("Ahmed", 20)

print(s1)

print(repr(s1))

print(s1 == s2)

print(s1 == s3)