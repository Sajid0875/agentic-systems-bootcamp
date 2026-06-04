def student():
    score = yield
    print("score is", score)

s = student()

next(s)      
s.send(90)  