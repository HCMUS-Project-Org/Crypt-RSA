
<h1>Cấu trúc file:</h1>
<pre>
19127525/
 |__Source/
 |   |__19127525.py
 |   |__plaintext01.txt
 |   |__plaintext02.txt
 |   |__encrypted.txt
 |   |__decrypted.txt
 |   |__QuansKey/
 |   |   |__rsa_pub.txt
 |   |   |__rsa.txt
 |__Report/
      |__19127525.pdf 
<pre/>

File có cấu trúc như sau cây thư mục ở trên
Trong đó báo cáo là file 19127525.pdf nằm ở ./19127525/Report/19127525.pdf
Các file mã nguồn nằm trong thư mục Source nằm ở ./19127525/Source gồm có:
<ul>
  <li> File thực thi 19127525.py</li>
  <li> Các file muốn encrypt/decrypt (file chứa plaintext, thực hiện nhiệm vụ 2 - 3) là file plaintext01.txt và plaintext02.txt <br>(2 file plaintext ví dụ) nằm cùng cấp với file thực thi </li>
  <li> 2 file encrypted.txt và decrypted.txt là 2 file mã hóa và giải mã plaintext ở trên, nằm cùng cấp với file thực thi </li>
  <li> Các cặp khóa sẽ được lưu trong 2 file rsa.txt và rsa_pub.txt vào thư mục con chứa khóa, ở đây là QuansKey (folder này là ví dụ).<br>Các folder chứa khóa này nằm cùng cấp với file thực thi </li>
</ul>

<h3>Hướng dẫn sử dụng và giải thích source code: <a href = './Report/19127525.pdf'>./Report/19127525.pdf</a> </h3>


