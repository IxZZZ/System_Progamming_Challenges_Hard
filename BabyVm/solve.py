file = open('vm_dump.vm', mode="rb")

str = file.read()
offset = 8

arr = []

for _ in range(len(str)):
    if(offset < len(str)):
        # if(str[offset]==7):
        arr.append(hex(str[offset])+ '-' + hex(str[offset+4]))
        # else:
        #     arr.append(hex(str[offset]))
        offset += 12

print(arr)
