class item:
    def __init__(self,members):
        self.members=members

    def __getitem__(self,index):
        return self.members[index]


item1=item(["Sajid","uzair","Ahmad"])

print(item1[0])  # Output: Sajid
print(item1[1])  # Output: uzair
print(item1[2])  # Output: Ahmad