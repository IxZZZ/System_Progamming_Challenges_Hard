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

      => hai điều kiện trên phải trái ngược nhau, khi `v3` số lần nhập là là 1,và 2 tương ưng với giá trị 0,1 thì điều kiện (`v3>1`) luôn sai nên sẽ không cần quan tâm tới điều kiện còn lại, Nếu `v3` số lần nhập là từ lần 3 trở đi (3,4,5) tương ứng với giá trị (2,3,4) thì điều kiện (`v3 > 1`) luôn đúng nên điều kiện còn lại (`v10`) phải bằng ko, mà `v10` sẽ bằng 0 khi `v7<=1` (ở trên thì `v7` được cộng lên khi mà câu lệnh `if ( v8 )` được thực hiện, nghĩa là từ lần nhập thứ 3 trở đi số lần thực hiện phép  `xor` trong mảng `a` phải ít nhất hai lần để `v7` > `1` và dẫn đến `v10` bằng `0`
  
  - sau khi đã nhập đủ `5` số và mảng `a` được xác định thì chương trình sẽ thực hiện vòng `while ( v11 != &a[31] );` để tính tổng các phần tử trong mảng `a`, cuối cùng tổng này đem so sánh với `0x40018038` nếu bằng nhau sẽ in ra chuỗi `Congrats`
  
  
  Tổng kết: 
  - Chương trình yêu cầu chúng ta nhập vào `5` số trong đó số tiếp theo sẽ phụ thuộc vào những số đã nhập trước đó
  - Sau đó thực hiện tìm vị trí bit `1` đầu tiền từ trái sang phải của giá trị nhập vào , lấy ra giá trị này ở trong mảng `a` nếu khác không sẽ đem `xor` với giá trị nhập vào , tiếp tục lặp để tìm vị trí bit `1` tiếp theo của số nhập vào, nếu vị trí này tiếp tục khác `0` thì sẽ tiếp tục `xor` thực hiện như trên, nếu vị trí khác `0` thì sẽ lưu kết quả phép `xor` vào vị trí này.
  - từ số thứ 3 nhập vào, chương trình sẽ kiểm tra số lần thực hiện phép `xor` ít nhất `2` lần, nghĩa là vị trí bit `1` của số nhập vào phải tương ứng với vị trí phần tử của mảng đã được lưu ở lần nhập trước đó, để được `xor` ít nhất `2` lần
  - cuối cùng sau khi nhập xong, sẽ so sánh tổng mảng `a` với `0x40018038`

Ở bài này, mình tận dụng tính chất hai số lệch nhau một đơn vị của một số sẽ có một số `xor` với số này sẽ bằng `1`, ví dụ (`5^4 = 1` và `5^6 = 3`)

Từ ý tưởng trên, ta có tổng mà ta muốn sẽ là `0x40018038` = `1073840184`, và để tận dụng được tính chất `xor` thì mảng `a` kết quả sẽ có hai phần tử là `1073840183` và `1` để tổng là kết quả cần tìm, và ta có `1073840183^1073840182 = 1` và do hai số này lệch nhau chỉ `1` đơn vị nên vị trí bit `1` đầu tiên sẽ như nhau, có nghĩa là:

- số đầu tiên nhập là `1073840183` vị trí bit `1` đầu tên sẽ là `31`, và số này được lưu ở vị trí `31` trong mảng `a`
- số thứ hai nhập là  `1073840182` vị trí bit `1` đầu tên cũng sẽ là `31` và số này sẽ được xor với số đầu tiên nhập vào và kết quả sẽ ra một và được lưu ở vị trí `1` trong mảng `a`
- số thứ 3,4,5 cũng sẽ là `1073840182` để cùng `xor` với giá trị đầu tiên nhập vào và kết quả ra `1` sẽ được `xor` với số tại vị trí `1` mà số này có giá trị `1` từ lần nhập thứ hai nên kết quả sẽ bằng `0` (`1^1`) nên sẽ không có lưu số nào mới từ lần nhập thứ `3` => không ảnh hưởng đến tổng mà ta muốn.

## Chạy chương trình với kết quả vừa tìm được

![image](https://user-images.githubusercontent.com/31529599/124370987-72e21380-dca7-11eb-8b1a-d92179dec7ad.png)

Xong !!!

