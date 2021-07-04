# **recurisve**

## Task:

File: CRACKME.exe

Chạy lệnh `file` để kiểm tra:

```bash
└─$ file CRACKME.exe
CRACKME.exe: PE32 executable (console) Intel 80386, for MS Windows
```

==> FIle windows 32 bits

Chạy thử chương trình:

```bash
└─$ ./CRACKME.exe
PASSWORD: hello
```


## Solution

Reverse file bằng IDA pro 32 bit

Vì code khá dài nên mình không để hết ở đây, chỉ trích ra một số hàm cần phân tích

Đây là hàm nhập vài `PASSWORD`

![image](https://user-images.githubusercontent.com/31529599/124371052-41b61300-dca8-11eb-9cd1-9e6168abf329.png)


Tiếp theo của đoạn code nhập vào sẽ là một đoạn code khoảng `400` dòng nhưng không có tác dụng gì cả ;)

Đây là đoạn tiếp theo mà ta cần quan tâm:

![image](https://user-images.githubusercontent.com/31529599/124371075-732ede80-dca8-11eb-8da0-353498934a53.png)

Hàm `call_to_win` đã được mình phân tích và đổi tên, hàm này sẽ truyền chuỗi chúng ta nhập vào và tiếp tục xử lý kiểm tra ở hàm này 

![image](https://user-images.githubusercontent.com/31529599/124371153-344d5880-dca9-11eb-9ae7-4ab5caf22983.png)

Chuỗi nhập vào được lưu ở `Src`

Mình thực hiện `References` đến hàm `print` ( hàm này cũng được mình đã đổi tên) thì thấy hàm này chỉ được gọi ở hai hàm, một là ở hàm `main` hai là ở hàm `call_to_win`, nên mình biết đây là vị trí in ra output mà mình cần

![image](https://user-images.githubusercontent.com/31529599/124371188-7b3b4e00-dca9-11eb-8bba-c641432f52ce.png)

Sau khi thực hiện debug và phân tích ngược từ vị trí in ra output thì mình thấy chỉ có đoạn này là ảnh hưởng đến flow của chương trình để in ra output, chỉ cần pass qua được đoạn `switch case` này là sẽ thành công:

```c
 if ( length_input_str )
  {
    while ( index_input )
    {
      switch ( index_input )
      {
        case 1:
          sub_DC2550(Block, &Src);
          v10 = Block;
          v9 = Block[0];
          if ( v69 >= 0x10 )
            v10 = (void **)Block[0];
          if ( *((_BYTE *)v10 + 1) != 't' )
          {
            if ( v69 < 0x10 )
              break;
            if ( v69 + 1 >= 0x1000 )
            {
              v9 = (void *)*((_DWORD *)Block[0] - 1);
              if ( (unsigned int)(Block[0] - v9 - 4) > 0x1F )
                goto LABEL_153;
            }
            goto LABEL_76;
          }
          if ( v69 < 0x10 )
            goto increase_v6_1;
          if ( v69 + 1 >= 0x1000 )
          {
            v9 = (void *)*((_DWORD *)Block[0] - 1);
            if ( (unsigned int)(Block[0] - v9 - 4) > 0x1F )
              goto LABEL_153;
          }
          goto increase_v6_2;
        case 2:
          sub_DC2550(Block, &Src);
          v11 = Block;
          v9 = Block[0];
          if ( v69 >= 0x10 )
            v11 = (void **)Block[0];
          if ( *((_BYTE *)v11 + 2) != 'o' )
          {
            if ( v69 < 0x10 )
              break;
            if ( v69 + 1 >= 0x1000 )
            {
              v9 = (void *)*((_DWORD *)Block[0] - 1);
              if ( (unsigned int)(Block[0] - v9 - 4) > 0x1F )
                goto LABEL_153;
            }
            goto LABEL_76;
          }
          if ( v69 < 0x10 )
            goto increase_v6_1;
          if ( v69 + 1 >= 0x1000 )
          {
            v9 = (void *)*((_DWORD *)Block[0] - 1);
            if ( (unsigned int)(Block[0] - v9 - 4) > 0x1F )
              goto LABEL_153;
          }
          goto increase_v6_2;
        case 3:
          sub_DC2550(Block, &Src);
          v12 = Block;
          v9 = Block[0];
          if ( v69 >= 0x10 )
            v12 = (void **)Block[0];
          if ( *((_BYTE *)v12 + 3) != 'p' )
          {
            if ( v69 < 0x10 )
              break;
            if ( v69 + 1 >= 0x1000 )
            {
              v9 = (void *)*((_DWORD *)Block[0] - 1);
              if ( (unsigned int)(Block[0] - v9 - 4) > 0x1F )
                goto LABEL_153;
            }
            goto LABEL_76;
          }
          if ( v69 < 0x10 )
            goto increase_v6_1;
          if ( v69 + 1 >= 0x1000 )
          {
            v9 = (void *)*((_DWORD *)Block[0] - 1);
            if ( (unsigned int)(Block[0] - v9 - 4) > 0x1F )
              goto LABEL_153;
          }
          goto increase_v6_2;
        case 4:
          sub_DC2550(Block, &Src);
          v13 = Block;
          v14 = Block[0];
          if ( v69 >= 0x10 )
            v13 = (void **)Block[0];
          if ( *((_BYTE *)v13 + 4) == 'i' )
          {
            if ( v69 >= 0x10 )
            {
              if ( v69 + 1 >= 0x1000 )
              {
                v14 = (void *)*((_DWORD *)Block[0] - 1);
                if ( (unsigned int)(Block[0] - v14 - 4) > 0x1F )
                  goto LABEL_153;
              }
              sub_DC4015(v14);
            }
increase_v6_1:
            ++v6;
            break;
          }
          if ( v69 >= 0x10 )
          {
            if ( v69 + 1 >= 0x1000 )
            {
              v14 = (void *)*((_DWORD *)Block[0] - 1);
              if ( (unsigned int)(Block[0] - v14 - 4) > 0x1F )
                goto LABEL_153;
            }
            sub_DC4015(v14);
          }
          break;
        case 5:
          sub_DC2550(Block, &Src);
          v15 = Block;
          v9 = Block[0];
          if ( v69 >= 0x10 )
            v15 = (void **)Block[0];
          if ( *((_BYTE *)v15 + 5) == 't' )
          {
            if ( v69 >= 0x10 )
            {
              if ( v69 + 1 >= 0x1000 )
              {
                v9 = (void *)*((_DWORD *)Block[0] - 1);
                if ( (unsigned int)(Block[0] - v9 - 4) > 0x1F )
                  goto LABEL_153;
              }
              sub_DC4015(v9);
            }
            ++v6;
          }
          else if ( v69 >= 0x10 )
          {
            if ( v69 + 1 >= 0x1000 )
            {
              v9 = (void *)*((_DWORD *)Block[0] - 1);
              if ( (unsigned int)(Block[0] - v9 - 4) > 0x1F )
                goto LABEL_153;
            }
LABEL_76:
            sub_DC4015(v9);
            break;
          }
          break;
      }
LABEL_77:
      if ( ++index_input >= length_input_str )
        goto pre_win_2;
    }
    sub_DC2550(Block, &Src);
    v8 = Block;
    v9 = Block[0];
    if ( v69 >= 0x10 )
      v8 = (void **)Block[0];
    if ( *(_BYTE *)v8 != 's' )
    {
      if ( v69 < 0x10 )
        goto LABEL_77;
      if ( v69 + 1 >= 0x1000 )
      {
        v9 = (void *)*((_DWORD *)Block[0] - 1);
        if ( (unsigned int)(Block[0] - v9 - 4) > 0x1F )
          goto LABEL_153;
      }
      goto LABEL_76;
    }
    if ( v69 < 0x10 )
      goto increase_v6_1;
    if ( v69 + 1 >= 0x1000 )
    {
      v9 = (void *)*((_DWORD *)Block[0] - 1);
      if ( (unsigned int)(Block[0] - v9 - 4) > 0x1F )
        goto LABEL_153;
    }
increase_v6_2:
    sub_DC4015(v9);
    ++v6;
    goto LABEL_77;
  }
pre_win_2:
  if ( v6 == 6 )
  {
    v16 = (char *)&Src;
    v17 = length_input_str;
```

ở đây mình chỉ đề một đoạn code, vì những phần khác không quan trọng và không ảnh hưởng đến chương trình

Ở cuối đoạn code trên chương trình kiểm tra `v6 == 6` , flow chính của chương trình nằm chổ này, nếu `v6 != 6` thì chương trình sẽ không in ra gì cả , ngược lại thì chương trình sẽ in ra output

Phân tích lên trên thì ta thấy đoạn trên gồm hai phần chính là một đoạn `switch case` gồm `5` case (từ `1` đến `5`) và một đoạn code ngoài, và đặc biệt `v6` sẽ được tăng lên `1` trong mỗi `case` của `switch` và nếu điều kiện của đoạn code ngoài `switch case` đạt điều kiện thì `v6` cũng sẽ được tăng lên `1`

Vậy mỗi `case` tăng lên `1` thì `v6` sẽ là `5` và ở đoạn code ngoài tăng lên `1` nữa là tổng sẽ là `6` là kết quả chúng ta cần

Ta thấy, trong mỗi đoạn thì sẽ có một đoạn `if` kiểm tra một phần tử trong mảng với một ký tự nếu khác nhau thì đoạn code trong `if` được gọi và sẽ `break case` cho nên không thể tăng `v6` được

Vì vậy ở mỗi `case` các phần tử trong mảng nhập vào sẽ phải bằng với ký tự so sánh, cụ thể là 

case 1: `t`
case 2: `o`
case 3: `p`
case 4: `i`
case 5: `t`

và `swithc case` chỉ được gọi khi phần tử trong mảng là phần tử thứ `2` trở đi (index từ `1`) còn phần tử đầu tiên (index `0`) sẽ gọi đoạn code ngoài, cũng tương tự đoạn code ngoài sẽ so sánh với ký tự `s`

Vậy để `v6` bằng `6` thì chuỗi nhập vào sẽ là `stopit`

## Chạy chương trình nhập vào chuỗi vừa tìm được 

![image](https://user-images.githubusercontent.com/31529599/124371429-dd954e00-dcab-11eb-9ac3-2bdf275540cd.png)

Vẫn chưa thấy kết quả in ra màn hình, nên mình đã debug và thấy rằng, chuỗi được in ra file chứ ko phải in ra màn hình, và tên file sẽ được random

![image](https://user-images.githubusercontent.com/31529599/124371435-f3a30e80-dcab-11eb-9fd5-8247498756a0.png)

![image](https://user-images.githubusercontent.com/31529599/124371458-19c8ae80-dcac-11eb-9f10-bef50435400d.png)

Xong !!!


