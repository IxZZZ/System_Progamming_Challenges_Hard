# Catalina

## Task:

File: crackme

Chạy lên file để kiểm tra:

```bash
└─$ file crackme
crackme: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=4e67f827e2bb32da50b2ce98842c4a9e9fde0996, stripped
```

=> file linux 64 bit


Chạy thử file:

```bash
└─$ ./crackme
Welcome to crackme N1
Usage:
./crackme <password>
```

```bash
└─$ ./crackme AAAAAAA 
Invalid flag, try again
```

Bài này yêu cầu nhập đúng `password`, `password` được truyền thông qua tham số khi gọi hàm

## Solution

Reverse bằng IDA pro 64 bits

Pseudocode hàm `main` :

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  __int64 result; // rax
  int v4; // ebx
  const char *v5; // r12
  size_t v6; // rax
  size_t v7; // rax
  char v8[32]; // [rsp+10h] [rbp-100h] BYREF
  __int64 v9[4]; // [rsp+30h] [rbp-E0h] BYREF
  char v10; // [rsp+50h] [rbp-C0h]
  int v11[34]; // [rsp+60h] [rbp-B0h]
  const char *v12; // [rsp+E8h] [rbp-28h]
  int v13; // [rsp+F4h] [rbp-1Ch]
  int i; // [rsp+F8h] [rbp-18h]
  int v15; // [rsp+FCh] [rbp-14h]

  if ( a1 == 2 )
  {
    v12 = "JTQSRyZKSB05Dh9JgH6fQJIVjJ04UpA7ezxMIHcvpX6X70NJHW4xlxSHHMuLDjCJbzl9ITfgeLbTDLExZENyYrAzn7ehjAMuZf1siTB4HBLgyJ"
          "gpK38LHCq4UvpgqOxeoh72AVgDOYS8HU9xg";
    v11[0] = 4;
    v11[1] = 4;
    v11[2] = 5;
    v11[3] = 4;
    v11[4] = 2;
    v11[5] = 4;
    v11[6] = 3;
    v11[7] = 4;
    v11[8] = 2;
    v11[9] = 4;
    v11[10] = 6;
    v11[11] = 2;
    v11[12] = 4;
    v11[13] = 6;
    v11[14] = 2;
    v11[15] = 5;
    v11[16] = 5;
    v11[17] = 2;
    v11[18] = 3;
    v11[19] = 3;
    v11[20] = 5;
    v11[21] = 4;
    v11[22] = 2;
    v11[23] = 3;
    v11[24] = 4;
    v11[25] = 2;
    v11[26] = 2;
    v11[27] = 3;
    v11[28] = 3;
    v11[29] = 2;
    v11[30] = 4;
    v11[31] = 5;
    v9[0] = 0LL;
    v9[1] = 0LL;
    v9[2] = 0LL;
    v9[3] = 0LL;
    v10 = 0;
    v15 = 0;
    for ( i = 0; i <= 31; ++i )
    {
      *((_BYTE *)v9 + i) = v12[v15];
      v15 += v11[i] + 1;
    }
    sub_563CD1AD0482((__int64)v9, (__int64)v8, 32);
    v15 = 0;
    v13 = 0;
    while ( v15 <= 23 )
    {
      v8[v15] ^= 0x41u;
      v4 = (unsigned __int8)v8[v15];
      v5 = a2[1];
      v6 = strlen(v5);
      if ( v6 >= v15 )
        v7 = v15;
      else
        v7 = strlen(a2[1]);
      v13 += v4 == v5[v7];
      ++v15;
    }
    if ( v13 == 24 )
      puts("Congratulations !! you solved the first challenge.");
    else
      puts("Invalid flag, try again");
    result = 0LL;
  }
  else
  {
    puts("Welcome to crackme N1");
    printf("Usage:\n%s <password>\n", *a2);
    result = 0xFFFFFFFFLL;
  }
  return result;
}
```

Hoạt động chính của chương trình nằm ở đoạn này:

![image](https://user-images.githubusercontent.com/31529599/124356305-7b9eff00-dc3f-11eb-8ee1-a172dc2a0b28.png)

Đoạn code khá đơn giản, `password` nhập vào được lưu ở biến `a2`, trong vòng `while`, biến `a2` được gán cho `v5` 

Ở dưới ta có thể thấy để in ra chuỗi `Congratulations ... ` thì `v13==24` mà `v13` được tăng lên trong vòng `while` khi `v4==v5[v7]`

Trong đó `v4` là kết quả của từng phần tử trong mảng `v8` đem xor với `0x41`

`v5[v7]` là phần tử trong mảng `password` nhập vào.


Vậy giá trị của `password` nhập vào phải bằng với kết quả phép xor phần tử mảng `v8` và `0x41`

Ta có thể debug để xem giá trị của mảng `v8`

Đặt breakpoint ngay trước khi vào vòng while để kiểm tra `password`

![image](https://user-images.githubusercontent.com/31529599/124357175-56f95600-dc44-11eb-82f5-4851ef562915.png)

Đây là giá trị của tất cả phần tử trong mảng `v8`

![image](https://user-images.githubusercontent.com/31529599/124357232-a3dd2c80-dc44-11eb-9b22-7738e3c08ebe.png)


### Script python

Viết một đoạn script python để tính giá trị của mảng nhập vào:

```python

#
arr = [0x27, 0x2D, 0x20, 0x26, 0x3A, 0x73, 0x71, 0x73, 0x71, 0x1E, 0x32, 0x20,
       0x2F, 0x20, 0x1E, 0x32, 0x20, 0x72, 0x28, 0x25, 0x20, 0x7B, 0x68, 0x3C]

str = ''.join(chr(i^0x41) for i in arr)

print('result: ', str)
```

### Chạy script

![image](https://user-images.githubusercontent.com/31529599/124357326-1221ef00-dc45-11eb-8053-530e806e2c72.png)

==> vậy chuỗi nhập vào sẽ là: `flag{2020_sana_sa3ida:)}`

## Chạy chương trình với kết quả tìm được 

Vì chuỗi nhập vào chứa ký tự đặt biệt nên phải đặt dấu `\` trước để phân biệt đó là ký tự.

```bash
└─$ ./crackme flag{2020_sana_sa3ida:\)}
Congratulations !! you solved the first challenge.
```

Xong !!!
