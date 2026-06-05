class student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __repr__(self):
        return f"student('{self.name}',{self.age})"
s=student("Sajid",20)
print(repr(s))
