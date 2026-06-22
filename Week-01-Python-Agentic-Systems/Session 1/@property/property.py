class student:
    def __init__(self,name):
        self._name=name 

    def get_name(self):
        return self._name
    
    name=property(get_name)
    # we can also write it as name=property(lambda self:self._name) but it is not recommended because it is not readable and it is not easy to understand.
s=student("john")
print(s.name)
