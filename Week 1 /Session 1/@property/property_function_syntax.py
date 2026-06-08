# we first create the separte versions then connect them together using the property function
class Student:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    def delete_name(self):
        del self._name

    name = property(
        get_name,
        set_name,
        delete_name,
        "Student name property"
    )


s = Student("John")

print(s.name)      # getter

s.name = "Ali"     # setter
print(s.name)

del s.name         # deleter
