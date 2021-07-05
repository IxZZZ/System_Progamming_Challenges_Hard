file = open('vm_dump.vm', mode="rb")

file_content = file.read()


instructions = ['mov_reg_val', 'mov_reg_reg', 'mov_reg[mem]', 'mov[reg] val', 'mov_reg[reg]', 'mov[mem] val', 'mov[mem] reg', 'push_val', 'push_reg', 'push[reg]', 'pop_reg', 'pop[reg]', 'pop[mem]', 'add_reg_reg', 'add_reg_val', 'add_reg[mem]', 'add[reg] val', 'add[reg] reg', 'sub_reg_reg', 'sub_reg_val', 'sub_reg[mem]', 'sub[reg] val', 'sub[reg] reg', 'mul_reg_reg', 'mul_reg_val', 'mul_reg[mem]', 'mul[reg] val', 'mul[reg] reg', 'xor_reg_reg', 'xor_reg_val',
                'xor_reg[mem]', 'xor[reg] val', 'xor[reg] reg', 'and_reg_reg', 'and_reg_val', 'and_reg[mem]', 'and [reg] val', 'and [reg] reg', 'nop', 'nop', 'nop', 'nop', 'nop', 'not_reg', 'not [reg]', 'not [mem]', 'cmp_reg_reg', 'cmp_reg_val', 'cmp_reg[mem]', 'cmp[reg] val', 'nop', 'loop_back', 'label_address_to_jump', 'set 0 loop_back_address', 'jmp', 'jmp_label', 'jz_return_address', 'jz_label', 'jnz_return_address', 'jnz_label', 'putchar_reg', 'getchar','nop']

print('Length instrcutions: ', len(instructions))
for offset in range(8,len(file_content),12):
    if(offset < len(file_content)):

        # bytes_0 = file_content[offset]
        # if bytes_0<len(instructions):
        #     if instructions[bytes_0] != 'nop':
        #         bytes_4_8 = file_content[offset+4:offset+8]
        #         bytes_8_12 = file_content[offset+8:offset+12]

        #         bytes_4_8 = int.from_bytes(
        #             bytes_4_8, byteorder='little', signed=False)
        #         bytes_8_12 = int.from_bytes(
        #             bytes_8_12, byteorder='little', signed=False)

        #         print(instructions[bytes_0], bytes_4_8, bytes_8_12)
        bytes_0 = file_content[offset]

        if bytes_0 == 7:
            print(file_content[offset+4],end=',')
