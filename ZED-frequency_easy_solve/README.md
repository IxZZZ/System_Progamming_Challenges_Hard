# **ZED-frequency**

## Task

File: ZED-Frequency.bin

Chạy lệnh file để kiểm tra:

```bash
ZED-Frequency.bin: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=3e0bc53b0b5739a9f0c588fafc92ec6cfdde1b42, not stripped
```

==> File linux 64 bit

Chạy thử file:

```bash
└─$ ./ZED-Frequency.bin
usage: ./ZED-Frequency.bin <keyfile>
```

Tạo một file: `keyfile.txt` với nội dung `ABCD`

```bash
└─$ ./ZED-Frequency.bin keyfile.txt
the generated key is: 11110000000000000000000000
you failed!!
```

## Solution

Load file thực thi bằng IDA pro 64 bits và tiến hành reverse:

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int i; // [rsp+10h] [rbp-B0h]
  int v5; // [rsp+10h] [rbp-B0h]
  int j; // [rsp+14h] [rbp-ACh]
  FILE *stream; // [rsp+18h] [rbp-A8h]
  int v8[28]; // [rsp+20h] [rbp-A0h]
  char s1[40]; // [rsp+90h] [rbp-30h] BYREF
  unsigned __int64 v10; // [rsp+B8h] [rbp-8h]

  v10 = __readfsqword(0x28u);
  if ( argc <= 1 )
  {
    printf("usage: %s <keyfile>\n", *argv);
    exit(1);
  }
  stream = fopen(argv[1], "rt");
  for ( i = 0; i <= 25; ++i )
    v8[i] = 0;
  while ( 1 )
  {
    v5 = fgetc(stream);
    if ( v5 == -1 )
      break;
    if ( v5 <= 96 || v5 > 122 )
    {
      if ( v5 > '@' && v5 <= 'Z' )
        ++v8[v5 - 'A'];
    }
    else
    {
      ++v8[v5 - 'a'];
    }
  }
  printf("the generated key is: ");
  for ( j = 0; j <= 25; ++j )
  {
    printf("%d", (unsigned int)v8[j]);
    s1[j] = LOBYTE(v8[j]) + 48;
  }
  s1[26] = 0;
  putchar(10);
  if ( !strcmp(s1, "01234567890123456789012345") )
    puts("you succeed!!");
  else
    puts("you failed!!");
  return 0;
}
```


Đoạn code trên gồm hai phần chính, một phần là xử lý nội dung từ file input và đoạn tiếp theo là so sánh dữ liệu sau khi xử lí và tạo ra từ file input và so sánh với `key` có sẵn trong chương trình:

Đoạn đầu:

![image](https://user-images.githubusercontent.com/31529599/124357686-10592b00-dc47-11eb-9922-c6605637590b.png)

Đoạn trên sẽ thực hiện các hoạt động:

- đọc file vào `stream`
- khởi tọa giá trị ban đầu là `0` cho tất cả các phần tử của `v8`
- đọc từ ký tự từ `stream` và thực hiện tính toán mảng `v8`, mảng `v8` được tính như sau:
  - nếu ký tự là ký tự hoa ( `if ( v5 > '@' && v5 <= 'Z' )` ) thì giá trị sẽ được trừ cho `A` và cộng `v8` tại vị trí là giá trị kết quả sau khi đã trừ lên `1` đơn vị
  - nếu ký tự là chữ thường ( `else` ) thì giá trị sẽ được trừ cho `a` và cộng `v8` tại vị trí là giá trị kết quả sau khi trừ lên `1` đơn vị

Đoạn Tiếp theo:

![image](https://user-images.githubusercontent.com/31529599/124357838-c3298900-dc47-11eb-8e61-440051ad23ef.png)

Đoạn này sẽ thực hiện các hoạt động:
- lấy từ phần từ của mảng `v8` mới được tạo từ nội dung file nhập vào cộng với `48` (`0`) sau đó lưu vào mảng `s1`
- so sánh chuỗi `s1` với chuỗi key mặc định `01234567890123456789012345` nếu bằng nhau thì sẽ in ra `Succeed` ngược lại sẽ in ra `Failed.`


Ta thấy trong key mặc định chỉ chứa các ký tự `0,1,2,3,4,5,6,7,8,9`, nên phần từ trong mảng `v8` phải có giá trị tương ứng từ `1` đến `9` để khi cộng với `48` sẽ tương ứng với ký tự trong chuỗi key mặc định.

Ở Phần đầu, thì mỗi lần phần tử trong mảng `v8` chỉ tăng lên `1` đơn vị, cho nên giá trị của phần tử trong mảng `v8` sẽ được tăng lên  theo số ký tự nhập vào tương ứng với phần tử đó.

### Script python

Viết một đoạn script python để tính chuỗi nhập vào từ key mặc định:

```python
# default key in code
key = '01234567890123456789012345'

list_key = list(key)

print(list_key)

# caculate original input from default key
res = ''.join(int(list_key[i])*chr(i+ord('a')) for i in range(len(list_key)))

# write to file
f = open('keyfile.txt','w')

f.write(res)

print('result: ',res)
```
### Chạy script python 

![image](https://user-images.githubusercontent.com/31529599/124358254-b017b880-dc49-11eb-97db-28f8372a86ee.png)

Vậy chuỗi nhập vào sẽ là : `bccdddeeeefffffgggggghhhhhhhiiiiiiiijjjjjjjjjlmmnnnoooopppppqqqqqqrrrrrrrsssssssstttttttttvwwxxxyyyyzzzzz`

## Chạy chương trình với kết quả vừa tìm được 

![image](https://user-images.githubusercontent.com/31529599/124358219-82cb0a80-dc49-11eb-80ea-df4db600fc04.png)


Xong !!!


