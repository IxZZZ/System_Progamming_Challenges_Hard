arr = [2, 17, 88, 78, 83, 75, 79, 79, 93, 76]
arr = [141, 222, 159, 199, 207, 152, 222, 207,
       243, 220, 156, 216, 243, 193, 152, 243, 197]
x = 60
x = 172
arr.reverse()
for i in arr:
    print(chr(i ^ x), end='')
