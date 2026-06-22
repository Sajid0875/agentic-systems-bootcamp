class superclass:
    def __init_subclass__(cls):
        cls.default_name="inherited class"
    
class subclass(superclass):
    default_name="sub class"


print(subclass.default_name)   
