class Tool:

    register=[]

    def __init_subclass__(cls):
        cls.register.append(cls)

    
class Hammer(Tool):
        pass 

class Screwdriver(Tool):
        pass 

print(Tool.register)