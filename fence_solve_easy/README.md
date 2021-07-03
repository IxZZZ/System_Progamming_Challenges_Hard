# **fence**

## Task:

File: encryptor , readme.txt

Chạy lệnh `file` để kiểm tra:

```bash
└─$ file encryptor
encryptor: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=b417774ddd1cfb3521bac910a9128bd397e2fe9c, not stripped 
```

==> File linux 64 bits

Chạy thử chương trình:

```bash
└─$ ./encryptor
you must supply exactly one argument
```

```bash
┌──(ixz㉿DESKTOP-6LQVP4S)-[/mnt/…/RE challenges/Hard/Release_3/fence_solve_easy]
└─$ ./encryptor hello                                                                                 
lhleo
```

Nội dung file readme.txt

`the encrypted flag is: "arln_pra_dfgafcchsrb_l{ieeye_ea}"`

=> mục đích của chương trình muốn chúng ta xuất ra mảng `arln_pra_dfgafcchsrb_l{ieeye_ea}`

## Solution

Reverse file bằng IDA pro 64 bits

Pseudocode hàm `main` (pseudocode này đã được phân tích và đổi tên một số hàm để dễ dàng cho quá trình phân tích):

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  __int64 v3; // rax
  unsigned __int64 length_input_str; // rax
  char *v5; // rax
  unsigned __int64 v6; // rax
  char *v7; // rax
  unsigned __int64 v8; // rax
  char *v9; // rax
  __int64 v10; // rax
  char v12; // [rsp+17h] [rbp-F9h] BYREF
  unsigned __int64 i; // [rsp+18h] [rbp-F8h]
  unsigned __int64 j; // [rsp+20h] [rbp-F0h]
  unsigned __int64 k; // [rsp+28h] [rbp-E8h]
  char input_str[32]; // [rsp+30h] [rbp-E0h] BYREF
  char output_part_1_2[32]; // [rsp+50h] [rbp-C0h] BYREF
  char output_part_2[32]; // [rsp+70h] [rbp-A0h] BYREF
  char output_part_1_1[32]; // [rsp+90h] [rbp-80h] BYREF
  char output_part_1[32]; // [rsp+B0h] [rbp-60h] BYREF
  char output[40]; // [rsp+D0h] [rbp-40h] BYREF
  unsigned __int64 v22; // [rsp+F8h] [rbp-18h]

  v22 = __readfsqword(0x28u);
  if ( argc != 2 )
  {
    v3 = std::operator<<<std::char_traits<char>>(&std::cout, "you must supply exactly one argument", envp);
    std::ostream::operator<<(v3, &std::endl<char,std::char_traits<char>>);
    exit(-1);
  }
  std::allocator<char>::allocator(&v12, argv, envp);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(
    (__int64)input_str,
    (__int64)argv[1],
    (__int64)&v12);
  std::allocator<char>::~allocator(&v12);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(output_part_1_2);
  for ( i = 0LL; ; i += 3LL )
  {
    length_input_str = std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::length(input_str);
    if ( i >= length_input_str )
      break;
    v5 = (char *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator[](input_str, i);
    std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator+=(
      output_part_1_2,
      (unsigned int)*v5);
  }
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(output_part_2);
  for ( j = 1LL; ; j += 3LL )
  {
    v6 = std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::length(input_str);
    if ( j >= v6 )
      break;
    v7 = (char *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator[](input_str, j);
    std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator+=(
      output_part_2,
      (unsigned int)*v7);
  }
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(output_part_1_1);
  for ( k = 2LL; ; k += 3LL )
  {
    v8 = std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::length(input_str);
    if ( k >= v8 )
      break;
    v9 = (char *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator[](input_str, k);
    std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator+=(
      output_part_1_1,
      (unsigned int)*v9);
  }
  std::operator+<char>(output_part_1, output_part_1_1, output_part_1_2);
  std::operator+<char>(output, output_part_1, output_part_2);
  v10 = std::operator<<<char>(&std::cout, output);
  std::ostream::operator<<(v10, &std::endl<char,std::char_traits<char>>);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(output);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(output_part_1);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(output_part_1_1);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(output_part_2);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(output_part_1_2);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(input_str);
  return 0;
}
```

Code tuy dài và hơi rối nhưng bài này khá đơn giản, chỉ cần nhìn kĩ những phần đuôi của mỗi lệnh sẽ biết được mục đích của lệnh đó

Phân tích sơ lược hàm `main` ta có thể thấy, chỉ có hai chổ gọi hàm để in ra màn hình `cout`:

- chổ đầu tiền là in ra lỗi ko truyền vào tham số

![image](https://user-images.githubusercontent.com/31529599/124360028-b316a700-dc51-11eb-8bd8-803288d88cef.png)

- Chổ thứ hai là ở gần cuối chương trình:

![image](https://user-images.githubusercontent.com/31529599/124360036-c3c71d00-dc51-11eb-835a-4e8c9d83c9e8.png)


Cho nên mình đoán vị trí in thứ hai này sẽ là vị trí output của chương trình.

Và trong chổ in thứ hai này sẽ in ra biến `output` , nhưng trước đó biến `output` được tính toán từ :

- `output` được cộng từ `output_part_1` và `output_part_2` 
- trong đó `output_part_1` được cộng từ `ouput_part_1_1` và `output_part_1_2`

Tiếp tục phân tích ngược lên trên để xem các phần tạo thành `output` được tạo thành như thế nào :

Đây là phần tạo thành `output_part_1_2`:

![image](https://user-images.githubusercontent.com/31529599/124360202-b8c0bc80-dc52-11eb-9a70-64de356a601e.png)


Đây là phần tạo thành `output_part_2`:

![image](https://user-images.githubusercontent.com/31529599/124360240-e6a60100-dc52-11eb-9953-d0d0eb8a2aee.png)


Đây là phần tạo thành `output_part_1_1`:

![image](https://user-images.githubusercontent.com/31529599/124360256-f887a400-dc52-11eb-8ab5-f4cfcead5c13.png)

Các đoạn code tạo thành các phần của `output` đều tương tự nhau chỉ khác nhau ở giá trị khởi tạo của `i,j,k` lần lượt là `0,1,2`

Vậy có nghĩa là mỗi đoạn 3 ký tự, mỗi kí tự sẽ tương ứng với 3 phần của `output`

### Script python

```python
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
```


### Chạy script python 

![image](https://user-images.githubusercontent.com/31529599/124360623-fe7e8480-dc54-11eb-8550-b998419b3bdd.png)

## Chạy chương trình nhập vào chuỗi vừa tìm được 

![image](https://user-images.githubusercontent.com/31529599/124360636-16ee9f00-dc55-11eb-834d-de82c327a20a.png)

Xong !!!
