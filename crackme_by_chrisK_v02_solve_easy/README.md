# **crackme_by_chrisK_v02**

## Task:

File: crackme_by_chrisK_v02.exe

Chạy lênh file để kiểm tra:

```bash
└─$ file crackme_by_chrisK_v02.exe
crackme_by_chrisK_v02.exe: PE32 executable (console) Intel 80386, for MS Windows
```

==> File windows 32 bits

Chạy thử file:

```bash
└─$ ./crackme_by_chrisK_v02.exe
Enter Password: hello
Wrong                                                                                                                   
```


## Solution

Reverse file bằng IDA pro 32 bit:

Pseducode hàm `main`:

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int result; // eax
  int v4; // eax
  char *v5; // ebx
  char Str2[50]; // [esp+10h] [ebp-74h] BYREF
  char Str[50]; // [esp+42h] [ebp-42h] BYREF
  char *v8; // [esp+74h] [ebp-10h]
  signed int v9; // [esp+78h] [ebp-Ch]
  int i; // [esp+7Ch] [ebp-8h]

  __main();
  i = 0;
  v9 = 0;
  printf("Enter Password: ");
  scanf("%s", Str);
  if ( strlen(Str) > 9 && Str[5] == '.' )
  {
    printf("Enter password key: ");
    scanf("%s", Str2);
    while ( 1 )
    {
      v4 = i++;
      if ( !Str[v4] )
        break;
      ++v9;
    }
    v8 = (char *)malloc(4 * v9);
    srand(v9);
    for ( i = 0; i < v9; ++i )
    {
      v5 = &v8[4 * i];
      *(_DWORD *)v5 = rand() % v9 + v9 / -2;
    }
    magic(Str, v8);
    if ( !strcmp(mstring, Str2) )
    {
      printf("Nice!!");
      result = 0;
    }
    else
    {
      printf("Wrong");
      result = 1;
    }
  }
  else
  {
    printf("Wrong");
    result = 1;
  }
  return result;
}
```

Ta thấy ở đoạn này, chương trình sẽ có hai lần gọi hàm `scanf` tức là hai lần yêu cầu nhập, tuy nhiên để nhập được lần 2 thì ta phải đúng được câu lênh `if ( strlen(Str) > 9 && Str[5] == '.' )`

=> chuỗi nhập vào đầu tiên phải có độ dài lớn hơn `9` và phần tử thứ `6` (tại vị index `5`) phải là ký tự `.`

![image](https://user-images.githubusercontent.com/31529599/124359019-50bba780-dc4d-11eb-8e26-63249b5e3579.png)

Ta nhập chuỗi đầu sẽ là `aaaaa.aaaa`

Ở đoạn tiếp theo: 

![image](https://user-images.githubusercontent.com/31529599/124359200-20c0d400-dc4e-11eb-85f0-ad7132f68a7c.png)

Để in ra chuỗi `NICE` thì thì chuỗi thứ 2 nhập vào `Str2` phải bằng với chuỗi `mstring`, mà chuỗi `mstring` được tạo từ hàm `magic`

![image](https://user-images.githubusercontent.com/31529599/124359318-a3499380-dc4e-11eb-96e1-cb80b52f1464.png)

Tuy nhiên chúng ta không cần quan tâm, chỉ cần đặt breakpoint ngay trước khi gọi hàm `strcmp` và xem giá trị của chuỗi `mstring` ứng với giá trị `Str` (chuỗi thứ nhất nhập vào)

![image](https://user-images.githubusercontent.com/31529599/124359459-55815b00-dc4f-11eb-9a1b-9de06fca39ac.png)

![image](https://user-images.githubusercontent.com/31529599/124359469-629e4a00-dc4f-11eb-8df6-1abb25983a62.png)

vậy chuỗi thứ 2 sẽ là `]e^\`c/^^be`



