def count_upto(n):
    count = 1
    while count <= n:
        yield count
        count = count + 1
counter=count_upto(5)
for i in count_upto(5):
  print(i)    