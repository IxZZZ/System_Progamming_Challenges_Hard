str = '01234567890123456789012345'

list_str = list(str)

print(list_str)

res = ''.join(int(list_str[i])*chr(i+ord('a')) for i in range(len(list_str)))

print(res)