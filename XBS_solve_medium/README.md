# **XBS**

## Task

File: a.out

Chạy lệnh `file` để kiểm tra:

```bash
└─$ file a.out
a.out: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=e645bcadcc14569d7dda684c9fe11b20b1a40bff, for GNU/Linux 3.2.0, not stripped
```

==> File linux 64 bits

Chạy thử chương trình:

```bash
└─$ ./a.out
asdasd
Try again!
```


## Solution

Reverse file bằng IDA pro 64 bits

pseudocode hàm `main`:

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v3; // ebx
  int v4; // eax
  __int64 v5; // rcx
  char v6; // si
  int v7; // edx
  int v8; // er9
  bool v10; // cc
  _DWORD *v11; // rax
  int v12; // edx
  const char *v13; // rdi
  int input; // [rsp+4h] [rbp-14h] BYREF
  unsigned __int64 v16; // [rsp+8h] [rbp-10h]

  v3 = 0;
  v16 = __readfsqword(0x28u);
  do
  {
    __isoc99_scanf(&format__d, &input, envp);
    v4 = input;
    v5 = 30LL;
    v6 = 0;
    v7 = 0;
    while ( ((v4 >> v5) & 1) == 0 )
    {
LABEL_9:
      if ( v5-- == 0 )
      {
        if ( v6 )
          input = v4;
        goto LABEL_12;
      }
    }
    v8 = a[v5];
    if ( v8 )
    {
      ++v7;
      v4 ^= v8;
      v6 = 1;
      goto LABEL_9;
    }
    if ( v6 )
      input = v4;
    a[(int)v5] = v4;
LABEL_12:
    v10 = v7 <= 1;
    envp = (const char **)(unsigned int)(v7 - 1);
    if ( v10 && v3 > 1 )
    {
Wrong_Label:
      v13 = "Try again!";
      goto Win_Label;
    }
    ++v3;
  }
  while ( v3 != 5 );
  v11 = a;
  v12 = 0;
  do
    v12 += *v11++;
  while ( v11 != &a[31] );
  v13 = "Congrats!";
  if ( v12 != 0x40018038 )
    goto Wrong_Label;
Win_Label:
  puts(v13);
  return 0;
}
```


Chương trình được phân tích thành 2 phần chính:

- Phần đầu tiên:

![image](https://user-images.githubusercontent.com/31529599/124360890-7305f300-dc56-11eb-9af3-92de755a6e90.png)

Ở phần đầu tiên chương trình sẽ nhập vào từng giá trị số nguyên thông qua hàm `scanf` với format string `%d`, sau đó xử lí và kiểm tra giá trị này, nếu giá trị này hợp lệ sẽ được nhập tiếp giá trị mới trong vòng while cho đến khi nhập đủ `5` giá trị, sẽ thoát vòng `do  while ( v3 != 5 );`

Ở vòng while đầu tiên chương trình sẽ kiểm tra vị trí bit `1` đầu tiên trong giá trị nhập vào ở dang binary tính từ trái sang phải , dùng phép shift right để kiểm tra bằng cách dịch từ giá trị ban đàu là `30` sau đó trừ cho một sau mỗi lần dịch cho đên skhi gặp bit `1`

vị trí tìm ra sẽ là kết quả của `v5`

Sau đó lấy giá trị tại vị trí `v5` (trong mảng `a` ban đầu được khởi tạo cóa `30` phần tử có gái trị `0`) gán cho `v8` nếu giá trị của `v8` khác `0` sẽ thực hiện phép `xor` với giá trị vừa nhập vào,

Tiếp tục nhảy về vòng while (goto LABEL_9) ở trên và tìm bit `1` tiếp theo, nếu kết quả của `v8` bằng không thì sẽ thực hiện tiếp đoạn code bên dưới,

Đoạn code tiếp theo sẽ thực hiện gán giá trị nhập vào hoặc sau khi được xor tại vào trong mảng `a` tại vị trí cuối cùng xuất hiện bit `1`.

- Phần Tiếp theo:

![image](https://user-images.githubusercontent.com/31529599/124361340-d42ec600-dc58-11eb-8612-12f1ec606590.png)

Sau khi tính giá trị của mảng `a` sau mỗi lần nhận thì chương trình sẽ kiểm tra lần lược:

  - `v10` có bằng `1` và `v3` có lớn hơn `1`, để chương trình không in ra chuổi `Try again` câu `if ( v10 && v3 > 1 )` phải sai, nghĩa là `v10` phải bằng không hoặc `v3` > `1`

  => hai điều kiện trên phải trái ngược nhau khi `v3` (số lần nhập) , nên số lần nhập là từ 2 trở xuống (`v7<=1`) nghĩa là `v10 ==1` thì `v3` >



