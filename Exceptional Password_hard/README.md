# **Exceptional Password**

# Task

File: exceptional_pass.exe

Chạy lệnh file để kiểm tra:

```bash
└─$ file excepional_pass.exe
excepional_pass.exe: PE32 executable (console) Intel 80386, for MS Windows
```

==> File windows 32 bits

Chạy thử chương trình

```bash
└─$ ./excepional_pass.exe
Enter the pass:
hello
Oh no! A password exception has occurred!
Enter the pass:
abcd
Oh no! A password exception has occurred!
Enter the pass:
xyz
Oh no! A password exception has occurred!
Enter the pass:
```


### Solution

Reverse file IDA pro 32 bit


**Lưu ý** : những đoạn code mình trích ra ở trong bài này, thì mình đã tiếng hành phân tích và đổi tiên để dễ hơn trong quá trình làm nên sẽ khác với IDA tự detect ra ban đầu

Pseudocode hàm `main`:

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  _DWORD eax3; // eax
  int result; // eax
  _DWORD var1C; // [esp+Ch] [ebp-1Ch]

  var1C = 100;
  while ( var1C )
  {
    print("Enter the pass: ");
    scanf("%14s", input_str);
    exception_fucntion_print_result();
    if ( eax3 )
      var1C = 0;
    else
      dword_154160 = 1;
  }
  return 0;
}
```

Hàm `main` chủ yếu chỉ là nhập vào `password` và được lưu ở biến `inpu_str` được lưu ở section `.data` nên có thể sử dụng ở nhiều hàm khác nhau (chuỗi nhập vào được format string giới hạn nhiều nhất `14` ký tự)

Quá trình xử lí chính của chương trình sẽ nằm trong hàm `exception_function_print_result`

Tuy nhiên khi xuất ra mã giả, thì IDA chỉ detect được có 1 dòng code:

![image](https://user-images.githubusercontent.com/31529599/124372041-e2f59700-dcb1-11eb-9c7a-3aae1485c258.png)

Là bởi vì luồng thực thi của chương trình này được người ta ra điều hướng theo `exception` nghĩa là trong hàm này thì người viết chương trình đã đặt sẵn một số chổ tự `throw exception` để luồng chương trình nhảy vào các hàm `handle` mà không tuân theo qui luật nhất định cho nên IDA không thể nào detect được ra mã gỉả

Bài này chỉ có thể phân tích bằng code asssembly:

Đây là graph view của phần mã giả của hàm `exception_function_print_result`

![image](https://user-images.githubusercontent.com/31529599/124372079-441d6a80-dcb2-11eb-88ff-75efb691687e.png)

Đây là hai `label` output của chương trình, ta có thể thấy không có đường flow nào trở trực tiếp tới hai label này, vì nó sẽ thực thực theo dạng `handle exception`

![image](https://user-images.githubusercontent.com/31529599/124372105-6f07be80-dcb2-11eb-94e6-b371b7dbcf02.png)

Xem references của hai `label` này:

![image](https://user-images.githubusercontent.com/31529599/124372145-ca39b100-dcb2-11eb-8e74-6c286f8f8b71.png)

![image](https://user-images.githubusercontent.com/31529599/124372149-d887cd00-dcb2-11eb-9977-2b859f790d72.png)

Ta thấy hai hàm này nằm trong cấu trúc struture của `exception` và loại `exception` này chính là `SHE` (Structured Handle Exception của win32), dùng ` _SCOPETABLE_ENTRY` để quản lí các `exception`

Mình đã tìm hiểu và biết được cách hoạt động của `SHE`: 

![image](https://user-images.githubusercontent.com/31529599/124372199-43390880-dcb3-11eb-87d6-4629f64a1f12.png)

Mỗi struct sẽ có 3 biến:

- Enclosing Level: là Level của exception cha ( nghĩa là exception này được lồng bởi một exception lớn khác)
- Filter Function : dùng để filter exception của hàm 
- Handle Function: dùng để xử lí chương trình khi có exception xảy ra

Tiến hành phân tích các chương trình khởi tạo exception trong hàm `exception_function_print_result` :

![image](https://user-images.githubusercontent.com/31529599/124372249-b6db1580-dcb3-11eb-9d33-a85777ac5382.png)

Đầu tiên, exception khởi tạo bằng 3 lệnh push:

- push    0FFFFFFFFh -> Try level của hàm body
- push    offset stru_389BC0 -> offset của `_SCOPETABLE_ENTRY`
- push    offset __except_handler3 -> loại exception (SHE3)

**Note**: `_SCOPETABLE_ENTRY` của hàm `exception_function_print_result` sẽ là `stru_389BC0`, tất cả các try level sẽ được tính từ vị trí này bắt đầu từ try level (0,1,2,3,...) tưởng ứng với các hàm `filter` và `handle` trong mỗi struct pointer

![image](https://user-images.githubusercontent.com/31529599/124372642-fa368380-dcb5-11eb-81dd-4ce1b0d1919d.png)


Tiếp tục debug và phân tích, ta sẽ thấy ngay chổ này, sẽ `throw` ra 1 `exception`, vì `dword_384160` nằm trong section `.rdata` (readonly data) nên không thể thay đổi giá trị được

![image](https://user-images.githubusercontent.com/31529599/124372600-a75ccc00-dcb5-11eb-99da-2e2356e7fd2c.png)

![image](https://user-images.githubusercontent.com/31529599/124372653-11757100-dcb6-11eb-8ffb-e64fb3b12439.png)


Và ngay trên vị trí `throw exception` thì `try level` được set là `2`, cho nên hàm handle sẽ nằm trong struct entry table tại vị trí index `2` từ offset `_SCOPETABLE_ENTRY` được khởi tạo ở trên

Là vị trí index `2` từ `stru_389BC0`, thì hàm handle sẽ là `loc_371227`

![image](https://user-images.githubusercontent.com/31529599/124372703-7cbf4300-dcb6-11eb-9d49-d75c77b20a64.png)

Tiếp tục debug:

![image](https://user-images.githubusercontent.com/31529599/124372787-4504cb00-dcb7-11eb-9f0c-d395141b5d33.png)

Continue debugging thì ta thấy chương trình đã nhảy đúng tới vị trí mà chúng ta đã phân tích và đặt break point, từ đây chương trình cũng xử lí exception tương tự như cách vừa xử lí exception đầu tiên như trên

![image](https://user-images.githubusercontent.com/31529599/124372873-f4da3880-dcb7-11eb-8a5b-49ae2d6686ab.png)

Ở đoạn code tiếp theo chương trình sẽ thực hiện một vòng `for` để duyện qua các ký tự ở vị trí chẵn trong mảng `byte_38B000` và lưu và mảng `save_new_arr`

![image](https://user-images.githubusercontent.com/31529599/124372895-189d7e80-dcb8-11eb-83d1-1fe29f0e1041.png)

Duyệt ký tự chẵn vì mỗi lần duyệt, sẽ tăng `eax` lên `2` và `eax` ban đầu có giá trị `0`

![image](https://user-images.githubusercontent.com/31529599/124372902-336ff300-dcb8-11eb-9582-bf36e3285590.png)

Sau khi chay vòng `for` `14` lần thì chương trình sẽ nhảy qua block bên trái:

![image](https://user-images.githubusercontent.com/31529599/124372937-7e8a0600-dcb8-11eb-826e-8a0328a0157f.png)

Và hiện tại chuỗi `save_new_arr` sẽ là `P@bbfb2`

![image](https://user-images.githubusercontent.com/31529599/124372946-95305d00-dcb8-11eb-81e8-6b96b53d6d99.png)


Ở phần code tiếp theo, Chương trình sẽ thực hiện truyền hai chuỗi `"P@bbfb2"` và chuỗi `"kb#fwj1"` vào hàm `sub_371000` và gọi hàm này, sau đó kiểm tra giá trị trả về trong `eax` có bằng không hay không và thực hiện rẻ nhánh đến block tương ứng

Từ đây ta sẽ phân tích sơ lược về cách chương trình gọi handel `label` để in ra kết quả :

![image](https://user-images.githubusercontent.com/31529599/124373035-5058f600-dcb9-11eb-8ed1-48c63f565f84.png)

Ta có thể thấy từ `offset _SCOPETABLE_ENTRY` được khởi tạo ban đầu, thì `try level` của hàm `win` là `3` và `try level` của hàm `fail` là `4`

Ta biết được trước khi gọi hàm `sub_371000` thì `try level` sẽ được set thành `3`, nếu `eax` kết quả trả về của hàm `sub_371000` bằng `0` thì sẽ nhảy đến `label loc_37129E` và thay đổi `try level` thành `4` và sau đó `throw exception` bằng dòng lệnh tiếp theo ngay sau đó khi thay đổi giá trị của biến trong section `readonly data`

Và khi `try level` bằng `4` thì sẽ gọi `label` handle `fail` cho nên bây giờ mục đích của chính ta là `eax` kết quả trả về sẽ bằng `1` và thực hiện đoạn code tiếp theo không thay đổi `try level` và throw exception tương tự bằng dòng code như trên, và gọi hàm handle `win`

Tiếp hành debug và nhảy vào hàm `sub_371000` để phân tích:

![image](https://user-images.githubusercontent.com/31529599/124373200-6adf9f00-dcba-11eb-81ce-8aac30520880.png)

Ngay ở đầu hàm này sẽ khởi tạo lại một `exception` mới cho hàm này với `offset` là `stru_389BA8`:

![image](https://user-images.githubusercontent.com/31529599/124373214-88ad0400-dcba-11eb-97fb-c3f89256ede8.png)

Ở dòng này, cũng tương tự sẽ `throw` ra `exception` bằng cách tương tự và sẽ gọi hàm `handle` trong `try level 0` từ offset khởi tạo của hàm này:

`Try Level` `0` sẽ có hàm `handle` là `loc_371046`, đặt break point tương tự như ở trên và debug tiếp nhảy đến hàm này:

![image](https://user-images.githubusercontent.com/31529599/124373246-e2153300-dcba-11eb-9412-1b45c94cbf4c.png)


![image](https://user-images.githubusercontent.com/31529599/124373291-54861300-dcbb-11eb-99b6-f176ec04607c.png)

Đoạn code này mục đích là so sánh `7` ký tự đầu tiên của chuỗi `input_str` nhập vào với `7` ký tự của chuỗi `kb#fwj1` được truyền hàm hàm `sub_371000` khi gọi hàm này.

Nếu có một ký khác chương trình sẽ nhảy đến hàm này và set `eax` bằng `0` sau đó trả về
![image](https://user-images.githubusercontent.com/31529599/124373356-ec83fc80-dcbb-11eb-9531-8619e0141b37.png)

Nếu tất cả các ký tự đều đúng, Chương trình sẽ nhảy tới block `loc_371097`:

![image](https://user-images.githubusercontent.com/31529599/124373393-30770180-dcbc-11eb-9ff8-12f1c46489e4.png)

Block này sẽ thực hiện thay đổi `try level` thành `1` và `throw exception` tương tư như những cách ở trên

Ta tiếp tục xem tại `try level` `1` sẽ tương ứng với hàm handle `loc_3710B7`:

![image](https://user-images.githubusercontent.com/31529599/124373446-687e4480-dcbc-11eb-8959-42de67d30640.png)

Tuy nhiên hàm này cũng khá đơn giản và tương thư như hàm trên nên mình cũng ko cần debug, hàm này sẽ so sánh tiếp `7` ký tự tiếp theo của `input_str` và chuỗi `P@bbfb2` (tham số thứ 2 truyền vào của hàm `sub_371000`)

![image](https://user-images.githubusercontent.com/31529599/124373495-db87bb00-dcbc-11eb-9faa-c1a0c362fe4d.png)

Nếu sai , cũng tương tự sẽ set `eax` bằng `0` và trả về

![image](https://user-images.githubusercontent.com/31529599/124373510-fbb77a00-dcbc-11eb-8220-354364f3b861.png)

Nếu đúng sẽ set `eax` bằng `1` và trả về

Vậy chuỗi chúng ta cần nhập sẽ là `kb#fwj1P@bbfb2`

## Chạy chương trình và nhập vào chuỗi vừa tìm được 

![image](https://user-images.githubusercontent.com/31529599/124373530-26a1ce00-dcbd-11eb-8ac6-f568aa531571.png)

Xong !!!








