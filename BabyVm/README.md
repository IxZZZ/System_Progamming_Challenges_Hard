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

Hàm này dễ đọc mỗi offset `12` bytes trong `Buffer` bắt đầu từ `bytes thứ 8` sau đó truyền vào hàm `main_switch_case`

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
case 0 -> mov_reg_val
case 1 -> mov_reg_[mem]
case 2 -> mov_[reg]_val
case 3 -> mov_reg_[reg]
case 4 -> mov_[mem]_val
case 5 -> mov_[mem]_reg
case 6 -> push
case 7 -> push
case 8 -> push
case 9 -> pop
case 10 -> pop 
case 11 -> pop
case 12 -> add_reg_reg
case 13 -> add_reg_val
case 14 -> add_reg_[mem]
```

