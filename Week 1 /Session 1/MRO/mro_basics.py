class parent ():
    def greet(self):
        print("hello from parent")

class child(parent):
   pass
              

obj=child()
obj.greet()
print(child.mro())