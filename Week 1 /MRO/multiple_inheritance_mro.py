class A:
    def method(self):
        print("method from class A")

class B(A):
     def fun(self):
        print("Method found in class B")


class C(A):
    def fun(self):
        print("Method found in class C")


class D(B, C):
    pass


obj = D()

print("Calling obj.fun():")
obj.fun()

for cls in D.mro():
    print(cls.__name__)