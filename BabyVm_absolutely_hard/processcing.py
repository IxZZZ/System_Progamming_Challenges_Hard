def replace_space(s):
    s = list(s)
    for i in range(len(s)):
        if s[i]==' ' and s[i-1].isalpha() and s[i+1].isalpha():
            s[i] = '_'
    
    return ''.join(s)
file = open('opcode.txt','r')

content = file.read()

instructions = content.split('\n')

print(len(instructions))
write_file = open('opcode_proccessed.txt','w')
for i in range(len(instructions)):
    instruct = replace_space(instructions[i])
    write_file.write('Case ' + str(i) + ' -> ' + instruct + '\n')
    #write_file.write("'" + instruct + "'" + ',')
