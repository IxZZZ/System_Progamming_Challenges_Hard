# **BabyVm**

## Task

File: VirtualMachine.exe

Chạy lệnh `file` để kiểm tra:

```bash
└─$ file VirtualMachine.exe
VirtualMachine.exe: PE32 executable (console) Intel 80386, for MS Windows
```

==> file windows 32 bits

Chạy thử Chương trình :

![image](https://user-images.githubusercontent.com/31529599/124443363-cf2c5c80-dda7-11eb-86ba-b6763bab7b1e.png)

## Solution

Reverse file bằng IDA pro 32 bit

Pseudocode hàm `main`

Một số tên hàm và biến đã được mình đổi tên để quá trình phân tích có thể dễ dàng hơn

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v3; // eax
  void *Buffer; // [esp+8h] [ebp-8h]
  FILE *Stream; // [esp+Ch] [ebp-4h] BYREF

  v3 = print(std::cout, "V1r7u41 M4ch1n3 by <@shockbyte>");
  std::ostream::operator<<(v3, align_output_and_fflush);
  Stream = 0;
  Buffer = allocator_func_new(0x53Cu);
  fopen_s(&Stream, "vm_dump.vm", "rb");
  if ( !Stream )
    exit(0);
  fread_s(Buffer, 0x53Cu, 1u, 0x53Cu, Stream);
  fclose(Stream);
  sub_2E38E0((void **)&save_buffer, Buffer, 1340u);
  sub_2E3820(&save_buffer);
  j_j_free(Buffer);
  system("\r\npause");
  return 0;
}
```

Hàm `main` chỉ có nhiệm vụ đọc file `vum_dump.vm` và lưu vào `Buffer`

Các hoạt động chính của chương trình này, nằm ở hàm `sub_2E3820`

```c
_DWORD *__thiscall sub_2E3820(_DWORD *this)
{
  _DWORD *result; // eax
  _BYTE *v2; // [esp+4h] [ebp-8h]

  this[12] = this[6] + 8;
  do
  {
    v2 = (_BYTE *)this[12];
    main_switch_case(this, v2);
    result = this;
    this[12] += 12;
  }
  while ( *v2 != '?' );
  return result;
}
```

Hàm này sẽ đọc mỗi offset `12` bytes trong `Buffer` bắt đầu từ `bytes thứ 8` sau đó truyền vào hàm `main_switch_case`

```c
unsigned __int8 __thiscall main_switch_case(_DWORD *this, _BYTE *a1)
{
  unsigned __int8 result; // al

  result = (unsigned __int8)a1;
  switch ( *a1 )
  {
    case 0:
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
    case 6:
      result = (unsigned __int8)sub_2E4600(this, a1);
      break;
    case 7:
    case 8:
    case 9:
      result = (unsigned __int8)sub_2E4D70(this, a1);
      break;
    case 0xA:
    case 0xB:
    case 0xC:
      result = sub_2E4CB0(a1);
      break;
    case 0xD:
    case 0xE:
    case 0xF:
    case 0x10:
    case 0x11:
      result = sub_2E3F40(a1);
      break;
    case 0x12:
    case 0x13:
    case 0x14:
    case 0x15:
    case 0x16:
      result = (unsigned __int8)sub_2E4E40(this, a1);
      break;
    case 0x17:
    case 0x18:
    case 0x19:
    case 0x1A:
    case 0x1B:
      result = sub_2E4790(a1);
      break;
    case 0x1C:
    case 0x1D:
    case 0x1E:
    case 0x1F:
    case 0x20:
      result = (unsigned __int8)sub_2E5040(this, a1);
      break;
    case 0x21:
    case 0x22:
    case 0x23:
    case 0x24:
    case 0x25:
      result = sub_2E4140(this, a1);
      break;
    case 0x2B:
    case 0x2C:
    case 0x2D:
      result = sub_2E49A0(a1);
      break;
    case 0x2E:
    case 0x2F:
    case 0x30:
    case 0x31:
      result = sub_2E4340(this, a1);
      break;
    case 0x33:
    case 0x34:
    case 0x35:
      result = sub_2E44C0(this, (int)a1);
      break;
    case 0x36:
    case 0x37:
      result = (unsigned __int8)sub_2E4520(this, a1);
      break;
    case 0x38:
    case 0x39:
      result = sub_2E45B0((int)this, a1);
      break;
    case 0x3A:
    case 0x3B:
      result = sub_2E4560((int)this, a1);
      break;
    case 0x3C:
      result = print_a_char((int)a1);
      break;
    case 0x3D:
      result = get_char(this, (int)a1);
      break;
    default:
      return result;
  }
  return result;
}
```

Sau khi phân tích thì mình biết được cách chương trình hoạt động sẽ là đọc mỗi `12 bytes` từ file `vm_dump.vm` sau đó hàm `main_switch_case` sẽ sử dụng giá trị của `12 bytes` này để điều hướng các hoạt động của chương trình. Phân tích sơ lược và lướt qua hầu hết các hàm trong các `case` switch thì mình thấy cách mà chương trình hoạt động ở mỗi case đều tương tự nhau bằng cách thao thao với `12 bytes` , thao tác chủ yếu với 2 giá trị (32 bits - 4 bytes)  `bytes 4 -> 8` và bytes `bytes 8 -> 12`

Từ đây mình đoán bài `virtual machine` này sẽ dùng code để giả lập lại bộ mã `assembly` đó là `12 bytes` này biểu thị cho một instruction và dùng các `switch case` để điều hướng, cùng tiếp tục phân tích ...

Ở đây mình sẽ bắt đầu phân tích từng `case` của switch, tuy nhiên code rất dài nên một số hàm mình sẽ chỉ giải thích sơ lược , chứ ko giải thích kĩ.

Biến `this` sẽ là địa chỉ của bytes đầu tiên trong `12 bytes`, bytes đầu tiên sẽ được truyền vào switch case của hàm `main_switch_case`

### Case 0 -> 6

Đây là hàm mà switch case 0 -> 6 gọi

```c
unsigned __int8 *__thiscall sub_2E4600(void *this, unsigned __int8 *a2)
{
  unsigned __int8 *result; // eax
  int v3; // [esp+0h] [ebp-30h] BYREF
  int v4; // [esp+4h] [ebp-2Ch] BYREF
  int v5; // [esp+8h] [ebp-28h] BYREF
  int v6; // [esp+Ch] [ebp-24h] BYREF
  int v7; // [esp+10h] [ebp-20h] BYREF
  int v8; // [esp+14h] [ebp-1Ch] BYREF
  int v9; // [esp+18h] [ebp-18h] BYREF
  int v10; // [esp+1Ch] [ebp-14h] BYREF
  int v11; // [esp+20h] [ebp-10h]
  _DWORD *v12; // [esp+24h] [ebp-Ch]
  unsigned __int8 v13; // [esp+28h] [ebp-8h] BYREF
  unsigned __int8 v14; // [esp+29h] [ebp-7h] BYREF
  unsigned __int8 v15; // [esp+2Ah] [ebp-6h] BYREF
  unsigned __int8 v16; // [esp+2Bh] [ebp-5h] BYREF
  unsigned __int8 v17; // [esp+2Ch] [ebp-4h] BYREF
  unsigned __int8 v18; // [esp+2Dh] [ebp-3h] BYREF
  unsigned __int8 v19; // [esp+2Eh] [ebp-2h] BYREF
  unsigned __int8 v20; // [esp+2Fh] [ebp-1h] BYREF

  v12 = this;
  result = a2;
  v11 = *a2;
  switch ( v11 )
  {
    case 0:
      v20 = a2[4];
      result = set_byte_8_9_10_11(v12, &v20, (_DWORD *)a2 + 2);
      break;
    case 1:
      v19 = a2[8];
      v10 = get_bytes_8_9_10_11(v12, &v19);
      v18 = a2[4];
      result = set_byte_8_9_10_11(v12, &v18, &v10);
      break;
    case 2:
      v3 = get_bytes_from_7_plus_argument(a2 + 8);
      v13 = a2[4];
      result = set_byte_8_9_10_11(v12, &v13, &v3);
      break;
    case 3:
      v17 = a2[4];
      v9 = get_bytes_8_9_10_11(v12, &v17);
      result = (unsigned __int8 *)set_bytes_at_7_plus_argument(&v9, a2 + 8);
      break;
    case 4:
      v16 = a2[8];
      v8 = get_bytes_8_9_10_11(v12, &v16);
      v7 = get_bytes_from_7_plus_argument(&v8);
      v15 = a2[4];
      result = set_byte_8_9_10_11(v12, &v15, &v7);
      break;
    case 5:
      v6 = a2[4];
      result = (unsigned __int8 *)set_bytes_at_7_plus_argument(&v6, a2 + 8);
      break;
    case 6:
      v14 = a2[8];
      v5 = get_bytes_8_9_10_11(v12, &v14);
      v4 = a2[4];
      result = (unsigned __int8 *)set_bytes_at_7_plus_argument(&v4, &v5);
      break;
    default:
      return result;
  }
  return result;
}
```

Đây là code hàm `sub_2E4600` , hàm này sẽ có `6` case cho, mỗi case sẽ tương ứng với các lệnh gán giá trị , như các hàm mình đã đổi tên thì có thể biết được rằng hàm này sẽ sử dụng cho lệnh `mov` trong đó:
- có 4 lệnh là dùng để gán giá trị thanh ghi cho thanh ghi với gọi hàm `set_byte_8_9_10_11`
- hai hàm còn lại sẽ gán giá trị thanh ghi cho vùng nhớ với gọi hàm `set_bytes_at_7_plus_argument`

Từ đây mình đổi tên `sub_2E4600` thành `mov`

==> `Case 1 -> 6 : mov`

Từ ý tưởng của `Case` đầu tiên, mình tiến hành phân tích tương tự các hàm `case` còn lại được kết quả như sau

Đây là hàm `main_switch_case` sau khi đã được phân tích và đổi tên


```
unsigned __int8 __thiscall main_switch_case(_DWORD *this, _BYTE *a1)
{
  unsigned __int8 result; // al

  result = (unsigned __int8)a1;
  switch ( *a1 )
  {
    case 0:
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
    case 6:
      result = (unsigned __int8)move(this, a1);
      break;
    case 7:
    case 8:
    case 9:
      result = (unsigned __int8)push(this, a1);
      break;
    case 0xA:
    case 0xB:
    case 0xC:
      result = pop(this, (int)a1);
      break;
    case 0xD:
    case 0xE:
    case 0xF:
    case 0x10:
    case 0x11:
      result = (unsigned __int8)add(this, a1);
      break;
    case 0x12:
    case 0x13:
    case 0x14:
    case 0x15:
    case 0x16:
      result = (unsigned __int8)sub(this, a1);
      break;
    case 0x17:
    case 0x18:
    case 0x19:
    case 0x1A:
    case 0x1B:
      result = mul(a1);
      break;
    case 0x1C:
    case 0x1D:
    case 0x1E:
    case 0x1F:
    case 0x20:
      result = (unsigned __int8)xor(this, a1);
      break;
    case 0x21:
    case 0x22:
    case 0x23:
    case 0x24:
    case 0x25:
      result = and(this, a1);
      break;
    case 0x2B:
    case 0x2C:
    case 0x2D:
      result = not(a1);
      break;
    case 0x2E:
    case 0x2F:
    case 0x30:
    case 0x31:
      result = cmp(this, a1);
      break;
    case 0x33:
    case 0x34:
    case 0x35:
      result = loop_back(this, (int)a1);
      break;
    case 0x36:
    case 0x37:
      result = (unsigned __int8)jmp(this, a1);
      break;
    case 0x38:
    case 0x39:
      result = jz((int)this, a1);
      break;
    case 0x3A:
    case 0x3B:
      result = jnz((int)this, a1);
      break;
    case 0x3C:
      result = print_a_char((int)a1);
      break;
    case 0x3D:
      result = get_char(this, (int)a1);
      break;
    default:
      return result;
  }
  return result;
}
```


Tổng kết switch case:

```
Case 0 -> mov_reg_val
Case 1 -> mov_reg_reg
Case 2 -> mov_reg[mem]
Case 3 -> mov[reg] val
Case 4 -> mov_reg[reg]
Case 5 -> mov[mem] val
Case 6 -> mov[mem] reg
Case 7 -> push 
Case 8 -> push 
Case 9 -> push 
Case 10 -> pop 
Case 11 -> pop
Case 12 -> pop 
Case 13 -> add_reg_reg
Case 14 -> add_reg_val
Case 15 -> add_reg[mem]
Case 16 -> add[reg] val
Case 17 -> add[reg] reg
Case 18 -> sub_reg_reg
Case 19 -> sub_reg_val
Case 20 -> sub_reg[mem]
Case 21 -> sub[reg] val
Case 22 -> sub[reg] reg
Case 23 -> mul_reg_reg
Case 24 -> mul_reg_val
Case 25 -> mul_reg[mem]
Case 26 -> mul[reg] val
Case 27 -> mul[reg] reg
Case 28 -> xor_reg_reg
Case 29 -> xor_reg_val
Case 30 -> xor_reg[mem]
Case 31 -> xor[reg] val
Case 32 -> xor[reg] reg
Case 33 -> and_reg_reg
Case 34 -> and_reg_val
Case 35 -> and_reg[mem]
Case 36 -> and [reg] val
Case 37 -> and [reg] reg
Case 38 -> nop
Case 39 -> nop
Case 40 -> nop
Case 41 -> nop
Case 42 -> nop
Case 43 -> not_reg
Case 44 -> not [reg]
Case 45 -> not [mem]
Case 46 -> cmp_reg_reg
Case 47 -> cmp_reg_val
Case 48 -> cmp_reg[mem]
Case 49 -> cmp[reg] val
Case 50 -> nop
Case 51 -> loop_back (thực hiện lặp lại instruction hiện tại và lưu lại giá trị của instruction sau khi thoát vòng lặp bằng cách gán this[13] = this[12] )
Case 52 -> label_address_to_jump ( thực hiện thiết lập một label có vị trí để nhảy tới tại this[14] = this[12] + 12 * this[4]
Case 53 -> set_0_loop_back_address ( set loopback address bằng 0 , this[13] = 0)
Case 54 -> jmp (nhảy tới địa chỉ loopback this[12]=this[13])
Case 55 -> jmp_label (nhảy tới label label[12]=label[14])
Case 56 -> jz_return_address 
Case 57 -> jz_label 
Case 58 -> jnz_return_address 
Case 59 -> jnz_label
Case 60 -> putchar_reg
Case 61 -> getchar

```

hai hàm `push` và `pop` khá là phức tạp nên vì chỉ còn hai hàm này mình đã đoán nó là `push` và `pop`, và thử lần lượt



### Script python 

Từ những `case` switch phần tích được ở trên, ta sẽ viết một đoạn script python để build lại code assembly cho chương trình

```python
file = open('vm_dump.vm', mode="rb")

file_content = file.read()


instructions = ['mov_reg_val', 'mov_reg_reg', 'mov_reg[mem]', 'mov[reg] val', 'mov_reg[reg]', 'mov[mem] val', 'mov[mem] reg', 'push_val', 'push_reg', 'push[reg]', 'pop_reg', 'pop[reg]', 'pop[mem]', 'add_reg_reg', 'add_reg_val', 'add_reg[mem]', 'add[reg] val', 'add[reg] reg', 'sub_reg_reg', 'sub_reg_val', 'sub_reg[mem]', 'sub[reg] val', 'sub[reg] reg', 'mul_reg_reg', 'mul_reg_val', 'mul_reg[mem]', 'mul[reg] val', 'mul[reg] reg', 'xor_reg_reg', 'xor_reg_val',
                'xor_reg[mem]', 'xor[reg] val', 'xor[reg] reg', 'and_reg_reg', 'and_reg_val', 'and_reg[mem]', 'and [reg] val', 'and [reg] reg', 'nop', 'nop', 'nop', 'nop', 'nop', 'not_reg', 'not [reg]', 'not [mem]', 'cmp_reg_reg', 'cmp_reg_val', 'cmp_reg[mem]', 'cmp[reg] val', 'nop', 'loop_back', 'label_address_to_jump', 'set 0 loop_back_address', 'jmp', 'jmp_label', 'jz_return_address', 'jz_label', 'jnz_return_address', 'jnz_label', 'putchar_reg', 'getchar','nop']

print('Length instrcutions: ', len(instructions))
for offset in range(8,len(file_content),12):
    if(offset < len(file_content)):

        bytes_0 = file_content[offset]
        if bytes_0<len(instructions):
            if instructions[bytes_0] != 'nop':
                bytes_4_8 = file_content[offset+4:offset+8]
                bytes_8_12 = file_content[offset+8:offset+12]

                bytes_4_8 = int.from_bytes(
                    bytes_4_8, byteorder='little', signed=False)
                bytes_8_12 = int.from_bytes(
                    bytes_8_12, byteorder='little', signed=False)

                print(instructions[bytes_0], bytes_4_8, bytes_8_12)

```

### Chạy script python 

```
push_val 2 0
push_val 17 0
push_val 88 0
push_val 78 0
push_val 83 0
push_val 75 0
push_val 79 0
push_val 79 0
push_val 93 0
push_val 76 0
mov_reg_val 0 10
mov_reg_val 1 60
loop_back 0 0
pop_reg 2 0
xor_reg_reg 2 1
putchar_reg 2 0
sub_reg_val 0 1
cmp_reg_val 0 0
jnz_return_address 0 0
set 0 loop_back_address 0 0
push_val 141 0
push_val 222 0
push_val 159 0
push_val 199 0
push_val 207 0
push_val 152 0
push_val 222 0
push_val 207 0
push_val 243 0
push_val 220 0
push_val 156 0
push_val 216 0
push_val 243 0
push_val 193 0
push_val 152 0
push_val 243 0
push_val 197 0
mov_reg_val 0 17
push_reg 0 0
loop_back 0 0
getchar 0 0
sub_reg_val 0 1
cmp_reg_val 0 0
jnz_return_address 0 0
label_address_to_jump 16 0
set 0 loop_back_address 0 0
pop_reg 0 0
mov_reg_val 1 0
loop_back 0 0
mov_reg[reg] 2 1
xor_reg_val 2 172
pop_reg 3 0
cmp_reg_reg 3 2
jnz_label 0 0
add_reg_val 1 1
sub_reg_val 0 1
cmp_reg_val 0 0
jnz_return_address 0 0
label_address_to_jump 4 0
jmp_label 0 0
push_val 49 0
push_val 54 0
push_val 70 0
push_val 8 0
push_val 86 0
push_val 100 0
push_val 8 0
push_val 14 0
push_val 73 0
push_val 8 0
push_val 77 0
push_val 8 0
push_val 73 0
push_val 100 0
push_val 12 0
push_val 85 0
push_val 11 0
push_val 95 0
push_val 100 0
push_val 8 0
push_val 126 0
push_val 15 0
push_val 8 0
push_val 10 0
push_val 75 0
push_val 64 0
push_val 121 0
push_val 115 0
push_val 104 0
push_val 5 0
push_val 22 0
push_val 92 0
push_val 90 0
push_val 87 0
push_val 93 0
mov_reg_val 0 35
mov_reg_val 1 59
loop_back 0 0
pop_reg 2 0
xor_reg_reg 2 1
putchar_reg 2 0
sub_reg_val 0 1
cmp_reg_val 0 0
jnz_return_address 0 0
set 0 loop_back_address 0 0
```

từ đây mình sẽ sơ lược qua luông của chương trình từ đoạn asm trên: 
- Đầu tiên chương trình sẽ `push` lần lược các giá trị `2,17,88,78,83,75,79,79,93,76`, sau đó dùng vòng lặp `loop_back` để `pop` giá trị này ra khỏi stack và `xor` với `60` sau đó gọi `putchar` in ra màn hình 

![image](https://user-images.githubusercontent.com/31529599/124488967-abced500-ddda-11eb-9c11-0571b62ef411.png)

Dùng đoạn code python này để xem giá trị của chuỗi in ra màn hình, chính là chuỗi yêu cầu nhập vào password (vì là stack nên thứ tự sẽ ngược lại)

![image](https://user-images.githubusercontent.com/31529599/124489118-dc167380-ddda-11eb-9cad-b8fd41098ccd.png)

- Ta thấy chuỗi tiếp theo cũng đươc `push` và stack
- Tiếp theo là một đoạn loop_back để gọi hàm `get_char` nhập vào ký tự
- ngay sau đó tiếp tục là một đoạn look_back, tuy nhiên đoạn này sẽ lấy giá trị `pop` ra từ stack của chuỗi nhập vào đem `xor` với `172` và so sánh với chuỗi được nhập vào 
Dùng đoạn python trên tương tự với chuỗi này xor với 172

![image](https://user-images.githubusercontent.com/31529599/124490161-fbfa6700-dddb-11eb-8cff-90485f71c8e5.png)

được chuỗi `i_4m_t0p_cr4ck3r!` -> ta đoán chuỗi này là chuỗi cần tìm 

## Nhập thử chuỗi 

![image](https://user-images.githubusercontent.com/31529599/124490336-2a784200-dddc-11eb-9350-fc47eb6e5cdb.png)

Vậy chuỗi nhập vào đã đúng và flag là `SHB{p134E3_d0n7_r3v3r53_m3}`


