str = ''
output_str = 'arln_pra_dfgafcchsrb_l{ieeye_ea}'
len_str = len(output_str)


len_str_part_1_2 = 0
# define length for output_part_1_2 from length output string
for i in range(0, len_str, 3):
    len_str_part_1_2 += 1


str_part_2 = ''
len_str_part_2 = 0
# define length for output_part_2 from length output string
for i in range(1, len_str, 3):
    len_str_part_2 += 1


str_part_1_1 = ''
len_str_part_1_1 = 0
# define length for output_part_1_1 from length output string
for i in range(2, len_str, 3):
    len_str_part_1_1 += 1


# get output part from output string through length
str_part_1_1 = output_str[0:len_str_part_1_1]
str_part_1_2 = output_str[len_str_part_1_1:len_str_part_1_2+len_str_part_1_1]
str_part_2 = output_str[len_str_part_1_1+len_str_part_1_2:]


print('Output str: ', output_str)
print('str part 1 1: ', str_part_1_1)
print('str part 1 2: ', str_part_1_2)
print('str part 2: ', str_part_2)

str = 'X'*len_str
str = list(str)
index = 0

# Caculate input string from i,j,k = 0,1,2
for i in range(0, len_str, 3):
    str[i] = str_part_1_2[index]
    if i+1 < len_str:
        str[i+1] = str_part_2[index]
    if i+2 < len_str:
        str[i+2] = str_part_1_1[index]
    index += 1


print('Original str: ', ''.join(str))
