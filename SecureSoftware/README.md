# **SecureSoftware**

## Task:
File: SecureSoftwarev1.5.exe, Readme.txt

Chạy lệnh `file` để kiểm tra file:

```bash
└─$ file SecureSoftwarev1.5.exe
SecureSoftwarev1.5.exe: PE32 executable (console) Intel 80386 (stripped to external PDB), for MS Windows
```

==> file windows 32 bits

Chạy thử chương trình

![image](https://user-images.githubusercontent.com/31529599/124409370-624a9f80-dd72-11eb-8ba2-5afc43351e28.png)

![image](https://user-images.githubusercontent.com/31529599/124409403-6c6c9e00-dd72-11eb-94e0-3dc744bbc8b4.png)


Nội dung file `Readme.txt` chủ yếu là mô tả các yêu cầu của bài này, và kĩ thuật có thể được dùng trong bài này. Vì file này khá dài nên mình không hiển thị ra hết ở đây.

## Solution

Reverse file bằng IDA pro 32 bit

Pseudocode hàm `main`
```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  HANDLE hHandle; // [esp+0h] [ebp-10h]
  CHAR *lpDst; // [esp+4h] [ebp-Ch]

  sub_402480();
  lpDst = (CHAR *)malloc(0xFFu);
  ExpandEnvironmentStringsA("%USERPROFILE%", lpDst, 0xFFu);
  SetCurrentDirectoryA(lpDst);
  free(lpDst);
  beginthread(StartAddress, 0, (void *)1);
  if ( IsDebuggerPresent() )
    word_404024 = 1;
  hHandle = (HANDLE)beginthread(sub_401BD4, 0, 0);
  sub_4021C9(main);
  if ( argc > 1 )
  {
    word_407034 = 1;
    if ( !strcmp(argv[1], "-i") )
    {
      sub_401874();
    }
    else if ( !strcmp(argv[1], "-u") )
    {
      sub_40174F();
    }
    else
    {
      sub_401781(off_40400C[0]);
      MessageBoxA(0, Text, "Error undefined arg", 0x30u);
    }
    exit(0);
  }
  sub_4017BC();
  WaitForSingleObject(hHandle, 0xFFFFFFFF);
  return 0;
}
```

Ta thấy, ở bài này sử dụng 2 loại anti debugger đó là :
- `IsDebuggerPresent()` để kiểm tra debug 
- và, dùng thread điểm kiểm tra, trong hàm `StartAddress`, hàm này dùng thời gian để kiểm tra debug (khi debug thì thời gian sẽ không thể nào nhanh khi thực thi chương trình được)
![image](https://user-images.githubusercontent.com/31529599/124410207-2f091000-dd74-11eb-8788-d58114b776a0.png)

Tuy nhiên , bài này trong file `Readme.txt` cũng cho phép sử dụng `anti patching & debugging` nên mình đã sử dụng plugin `Patcher` trong IDA pro để patch lại chương trình ( thành lệnh `nop`)  để bypass anti debug

*Lưu ý*: bài này không những sử dụng 2 loại anti debug trên, mà còn sử dụng một hàm để check debug và sẽ làm sai kết quả khi phát hiện debug, sẽ được phân tích ở những phần tiếp theo

Pseudocode sau khi đã `Patch` và được phân tích đổi tên một số hàm cho dễ đọc ( hầu hết các hàm và các biết đã được mình đổi tên trong quá trình làm để dễ phân tích và sử dụng để viết write up dễ hơn)

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  HANDLE hHandle; // [esp+0h] [ebp-10h]
  CHAR *lpDst; // [esp+4h] [ebp-Ch]

  sub_402480();
  lpDst = (CHAR *)malloc(0xFFu);
  ExpandEnvironmentStringsA("%USERPROFILE%", lpDst, 0xFFu);
  SetCurrentDirectoryA(lpDst);
  free(lpDst);
  beginthread((_beginthread_proc_type)StartAddress, 0, (void *)1);
  IsDebuggerPresent();
  hHandle = (HANDLE)beginthread(check_key, 0, 0);
  check_break_point(main);
  if ( argc > 1 )
  {
    set_1_when_pass_argument = 1;
    if ( !strcmp(argv[1], "-i") )
    {
      initialize_function();
    }
    else if ( !strcmp(argv[1], "-u") )
    {
      undo_function();
    }
    else
    {
      calculate_TEXT_to_output(off_40400C[0]);
      MessageBoxA(0, Text, "Error undefined arg", 0x30u);
    }
    exit(0);
  }
  Error_function();
  WaitForSingleObject(hHandle, 0xFFFFFFFF);
  return 0;
}
```

Sơ lược về flow của hàm `main` (mình chỉ phân tích những hàm mà chúng ta cần quan tâm đến):
- Ngay trước đoạn dùng để anti debug là đoạn chương trình thiết lập lại thư mục hiện hành cho chương trình tại đường dẫn `%USERPROFILE%` chính là đường dẫn `C:\Users\(UserName)>` với UserName là tên user của hệ điều hành, với máy mình sẽ là `C:\Users\IxZ>`
- Sau đoạn anti debug sẽ là đoạn kiểm tra tham số truyền vào , nếu là:
  -  `-i` sẽ gọi hàm `initialize_function` -> hàm này dùng để nhập key và khởi tạp file authentication
  -  `-u` sẽ gọi hàm `undo_function` -> hàm này dùng để undo tất cả các bước đã thực hiện ở trên hệ thống bằng tham số `-i`
  -  Nếu tham số truyền vào không nằm trong hai tham số trên, thì sẽ gọi `MessageBox` in ra dòng trong `Text`, tuy nhiên thì như mình đã phân tích và đổi tên một hàm ngay trước khi gọi `MessageBox` là hàm `calculate_TEXT_to_output`, hàm này sẽ lấy tham số là một chuỗi trong section `.data` sau đó thực hiện duyệt chuỗi này , mỗi phần tử sẽ trừ đi một đơn vị và truyền vào TEXT
  ![image](https://user-images.githubusercontent.com/31529599/124411689-37af1580-dd77-11eb-88ff-2e497a03550d.png)
  
  ![image](https://user-images.githubusercontent.com/31529599/124411719-4990b880-dd77-11eb-811e-480ba8874b31.png)
  
  Mình đã thử viết đoạn code python để tính chuỗi tại vị trí truyền vào này sẽ có kết quả là :
  ![image](https://user-images.githubusercontent.com/31529599/124411809-6fb65880-dd77-11eb-9c5b-57621698e16e.png)
  Vậy đây là `MessageBox` show khi truyền vào tham số không xác định
- Nếu không truyền vào tham số thì chương trình sẽ gọi vào `Error_Function`, hàm này sẽ gọi `MessageBox` và in ra chuỗi lỗi bằng cách đã được phân tích ở trên, và đặc biệt ở đây sẽ gọi `WaitForSingleObject` cho hàm handle và thread của hàm handle là hàm `check_key` nên mình thử kiểm tra và biết được hàm này sẽ kiểm tra `authencication` file được tạo từ `initialize`, sẽ được phân tích ở dưới
![image](https://user-images.githubusercontent.com/31529599/124412072-eb180a00-dd77-11eb-8ffb-d67aecd16a4b.png)


Vậy ta biết chương trình sẽ sử dụng tham số `-i` để tạo key và không truyền tham số để check key

### Hàm initialize_function

Pseudocode :

```c
int initialize_function()
{
  int v1; // [esp+18h] [ebp-100h] BYREF
  char Buffer[219]; // [esp+1Ch] [ebp-FCh] BYREF
  FILE *Stream; // [esp+F8h] [ebp-20h]
  __time32_t v4; // [esp+FCh] [ebp-1Ch]
  unsigned int j; // [esp+100h] [ebp-18h]
  char *v6; // [esp+104h] [ebp-14h]
  unsigned int i; // [esp+108h] [ebp-10h]
  char *v8; // [esp+10Ch] [ebp-Ch]

  CreateDirectoryA(".\\data", 0);
  v4 = time(0);
  Stream = fopen(".\\data\\authdata.dat", "wb");
  if ( !Stream )
  {
    MessageBoxA(0, "File Access Error", "Error: Internal", 0x10u);
    exit(-2);
  }
  beginthread((_beginthread_proc_type)StartAddress, 0, 0);
  while ( !word_407036 )
    ;
  str_n_cpy(off_404008, Buffer, 6);
  str_n_cpy(off_404008, &Buffer[212], 6);
  *(_DWORD *)&Buffer[8] = v4;
  strcpy(&Buffer[12], UserName);
  strcpy(&Buffer[62], PCname);
  calculate_TEXT_to_output(off_404014[0]);
  printf("%s", Text);
  scanf("%100[^\n]", &Buffer[112]);
  if ( !Buffer[112] )
  {
    MessageBoxA(0, "Key can't be empty", "Error Input", 0x30u);
    fclose(Stream);
    undo_function();
    exit(0);
  }
  if ( dword_404040 )
  {
    v8 = Buffer;
    for ( i = 0; i <= 219; ++i )
      *v8++ = 0;
  }
  v1 = 0;
  v6 = Buffer;
  for ( j = 0; j <= 0xDB; ++j )
    v1 += (unsigned __int8)*v6++;
  fwrite(Buffer, 0xDCu, 1u, Stream);
  fclose(Stream);
  Stream = fopen(".\\data\\checksum", "wb");
  if ( !Stream )
  {
    undo_function();
    MessageBoxA(0, "File Access Error", "Error: Internal", 0x10u);
    exit(-2);
  }
  fwrite(&v1, 4u, 1u, Stream);
  return fclose(Stream);
}
```

Sơ lược flow của hàm này :
- đầu tiên hàm này sẽ tạo ra thư mục `data` trên thư mục hiện hành được set ở hàm main, sau đó tạo ra hai file `authdata.dat` và `checksum` trong thư mục `data`
- tiếp theo chương trình sẽ khởi tạo dữ liệu cho biến buffer như sau:
  - `Buffer[0-6]` là lưu chuỗi  `cv2pr` từ biến `off_404008`
  - `Buffer[8-12]` là lưu giá trị của `v4` là `time(0)`
  - `Buffer[12-62]` là lưu `UserName` (biến này được set ở 1 thread khác)
  - `Buffer[62-112]` là lưu `PcName` (biến này được set ở 1 thread khác)
  - `Buffer[112-212]` là lưu `Key` nhập vào từ `scanf`
  - `Buffer[212-219]` lưu chuỗi `cv2pr` từ biến `off_404008`
- Sau đó `Buffer` được ghi vào file `authdata.dat` 
- Cuối cùng file `checksum` sẽ lưu tổng các phần tử nằm trong mảng `Buffer`

mình vừa sơ lược toàn bộ hàm `initialize_function` để tạo key, sau đây sẽ phân tích tiếp hàm `check_key`

## Hàm check_key

Pseudocode của hàm `check_key` đã được mình chỉnh sửa hầu hết các tên hàm và tên biến có ảnh hưởng đến chương trình
```c
void __cdecl check_key()
{
  check_break_point(Error_function);
  check_break_point(initialize_function);
  get_usetname_pcname_ifnot_debug();
  if ( word_40703E )
  {
    if ( !set_1_when_pass_argument && (_WORD)default_2 == 2 )
    {
      check_break_point(0);
      sub_401F18();
      if ( !set_0_in_check_break_point
        && set_1_when_first_and_end_6_char_equal_with_cv2pr == 1
        && set_in_sub_401F18 == 1
        && !set_0_in_sub_401F18 )
      {
        calculate_TEXT_to_output(off_40401C[0]);
        MessageBoxA(0, Text, &byte_40524E, 0x40u);
        exit(0);
      }
    }
  }
}
```

Đầu tiên, cách để mình biết được đây là hàm dùng để check key như cái tên hàm mà mình đã đặt là vì mình xem chuỗi được truyền vào hàm `calculate_TEXT_to_output` (`off_40401C[0]`) để tính chuỗi `TEXT` được show bằng `MessageBox`, và kết quả:
![image](https://user-images.githubusercontent.com/31529599/124417840-46e89000-dd84-11eb-9a61-661f04b12445.png)

==> đây là chuỗi mà mình cần in ra, nên mình biết đây là hàm mình cần phân tích

Đầu tiên trong hàm này gọi hai hàm `check_break_point` cho hàm `Error_Function` và `initialize_function` , mục đích của hàm `check_break_point` sẽ là kiểm tra xem những hàm được truyền vào có được đặt `break point` bằng cách tính tổng các `opcode` của hàm cho đến khi gặp 7 lệnh `nop - 0x90` thì sẽ dừng tính tổng , sau đó sẽ so sánh với tổng ban đầu của hàm được lưu vào trong bộ nhớ, nếu tổng này khác nhau thì sẽ biết hàm này đang đặt break point (vì khi đặt break point thì chương trình sẽ thay đổi lệnh tại đó thành opcode `0xCC` dẫn đến tổng thay đổi), nếu không phát hiện breakpoint đang có thì một số biến sẽ được set cụ thể `dword_404040 = 0;` biến này nếu khác `0` thì sẽ ảnh hưởng đến `UserName` và `PcName` cụ thể là giá trị này sẽ được thay đổi thành `x`.

Như đã vừa phân tích, thì trong hàm `get_usetname_pcname_ifnot_debug`, sẽ thực hiện việc đó, nếu đang debug thì `UserName` và `PcName` truyền vào `Buffer` là `x`

![image](https://user-images.githubusercontent.com/31529599/124418487-c3c83980-dd85-11eb-94f3-afaf5af2341b.png)

Tiếp theo `if ( word_40703E )` thì biến `word_40703E` sẽ được set `1` nếu thư mục `data` tồn tại tại đường dẫn hiện hành trong hàm `Error_function` ( điều kiện trước khi check key là phải tạo key)

Tiếp theo `if ( !set_1_when_pass_argument && (_WORD)default_2 == 2 )` câu lệnh này sẽ luôn đúng nếu chúng ta ko truyền tham số khi chạy chương trình , như mình đã phân tích và đổi tên thì `set_1_when_pass_arguemnt` sẽ bằng `0` khi ko truyền tham số và biến `default_2` mặc định luôn bằng `2`

`check_break_point(0);` => khi tham số truyền vào hàm là địa chỉ của hàm thì nó sẽ check break point, nếu tham số truyền vào hàm là `0` thì nó sẽ kiểm tra file `checksum`, bằng cách tính tổng `Buffer` va so với tổng trong file checksum, nếu tổng khác nhau thì gọi hàm `undo_function` và xóa tất của các file và thư mục được tạo trong `initalize_function`

Trước khi phân tích hàm `Sub_401F18` ta phân tích câu lệnh `if` cuối cùng trước khi in ra chuỗi `Success, ...`:

`      if ( !set_0_in_check_break_point
        && set_1_when_first_and_end_6_char_equal_with_cv2pr == 1
        && set_in_sub_401F18 == 1
        && !set_0_in_sub_401F18 )
      {
`

tất cả các tên biến đã được mình đổi tên theo tính chất của nó, mình sẽ lần lượt đặt điều kiện 1,2,3,4 cho các điều kiện sau

- `1.` biến đầu tiên `set_0_in_check_break_point` sẽ được set khi không có breakpoint
- `2.` biến `set_1_when_first_and_end_6_equal_with_cv2pr` thì như cấu trúc của `Buffer` thì đầu kiện này sẽ luôn thoải nếu file `Authdata.dat` được tạo từ hàm `initialize_function`
- `3.` biến `set_in_sub_401F18` sẽ được phân tích trong hàm `sub_401F18`
- `4.` biến `set_0_in_sub_401F18` cũng tương tự như trên

## Hàm sub_401F18

Pseudocode của hàm này:

```c
int sub_401F18()
{
  _BOOL2 v0; // ax
  int result; // eax
  DWORD pcbBuffer; // [esp+10h] [ebp-F8h] BYREF
  char Buffer[219]; // [esp+14h] [ebp-F4h] BYREF
  int v4; // [esp+F0h] [ebp-18h]
  FILE *Stream; // [esp+F4h] [ebp-14h]
  int i; // [esp+F8h] [ebp-10h]
  int v7; // [esp+FCh] [ebp-Ch]

  Stream = fopen(".\\data\\authdata.dat", "rb");
  if ( !Stream )
  {
    calculate_TEXT_to_output((unsigned __int8 *)off_404020);
    MessageBoxA(0, Text, &byte_40524E, 0);
    exit(-1);
  }
  check_break_point(sub_401D0C);
  fread(Buffer, 0xDCu, 1u, Stream);
  compare_first_and_end_6_char_with_cv2pr(Buffer);
  Str = &Buffer[112];
  check_break_point(sub_401F18);
  beginthread((_beginthread_proc_type)StartAddress, 0, 0);
  v4 = strlen(Str);
  if ( !v4 )
    set_1_when_first_and_end_6_char_equal_with_cv2pr = 0;
  pcbBuffer = 100;
  GetUserNameA(UserName, &pcbBuffer);
  pcbBuffer = 100;
  GetComputerNameA(PCname, &pcbBuffer);
  v0 = strcmp(&Buffer[12], "x") && strcmp(&Buffer[62], "x");
  set_in_sub_401F18 = v0;
  if ( set_0_in_check_break_point )
  {
    dword_404040 = 2;
    get_usetname_pcname_ifnot_debug();
  }
  result = (unsigned __int16)set_1_when_first_and_end_6_char_equal_with_cv2pr;
  if ( set_1_when_first_and_end_6_char_equal_with_cv2pr )
  {
    sub_401D0C((int)Buffer);
    v7 = 0;
    for ( i = 0; i < v4; ++i )
    {
      if ( Str[i] != -1 )
      {
        calculate_TEXT_to_output((unsigned __int8 *)off_404018[0]);
        MessageBoxA(0, Text, &byte_40524E, 0x10u);
        v7 = 1;
        break;
      }
    }
    if ( v7 == 1 )
    {
      set_1_when_first_and_end_6_char_equal_with_cv2pr = 0;
      set_in_sub_401F18 = 0;
    }
    else
    {
      set_0_in_sub_401F18 = 0;
    }
    result = fclose(Stream);
  }
  else
  {
    set_0_in_sub_401F18 = 1;
  }
  return result;
}
```

Mục đích của hàm này là sẽ đọc file `authdata.dat` sau đó kiểm tra điều kiện nếu thỏa sẽ set các biến ở điều kiện `2,3,4`

Đầu tiên tại dòng `compare_first_and_end_6_char_with_cv2pr(Buffer);` sẽ set điều kiên `2`,luôn thoải nếu file được tạo từ `parameter -i`

Tiếp theo là hai dòng
`
  v0 = strcmp(&Buffer[12], "x") && strcmp(&Buffer[62], "x");
  set_in_sub_401F18 = v0;
`
nếu `Buffer[12]` và `Buffer[62]` tương ứng với `UserName` và `PcName` khác `x` nghĩa là `file` này không phải được tạo ra từ quá trình `debug` thì sẽ set `1` (kết quả của hàm strcmp nếu khác sẽ là -1 hoặc +1) cho biến `set_in_sub_401F18` => điều kiện `3` 

Tiếp theo sẽ là :
![image](https://user-images.githubusercontent.com/31529599/124419970-c710f480-dd88-11eb-89b9-b4652f690073.png)

