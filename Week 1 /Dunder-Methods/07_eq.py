class members:
    def __init__(self,name):
        self.name=name

    def __eq__(self, other):
            return self.name==other.name
        
s1 = members("Ali")
s2 = members("Ali")
s3 = members("Ahmed")

print(s1==s2)
print(s1==s3)
