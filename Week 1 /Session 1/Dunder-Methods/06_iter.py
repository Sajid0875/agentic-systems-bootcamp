class team:
    def __init__(self,members):
        self.members=members

        def __iter__(self):
            return iter(self.members)
        
team1=team(["sajid","abbas","ahmad"])

for member in team1:
    print(member)
        