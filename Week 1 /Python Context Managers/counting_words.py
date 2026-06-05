with open("file.txt")as file:
    text=file.read()
    n=0 
    for word in text.split():
        if word.lower() in ["the","and","is"]:
            n+=1
    print('words uses the, and, or is:',format(n))