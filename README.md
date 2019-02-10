# RawText2Mobi
网络小说生成mobi，将纯文本转换为mobi，配合小说爬虫
## 思路
1. 输入章节名和正文，生成单章HTML文件，并生成TOC.html
2. 写入电子书目录导航：NCX
  - 书名
  - 章节列表：由字典元素组成。
    - id
    - title
    - fileName
3. 写入电子书详情: OPF
  - Metadata：一些如书名、作者、出版社和装帧之类的信息。在 OPF 网站上有一个很全的 Metadata 列表供你引用。
  - Manifest：包含所有文件的列表（如 HTML 和 NCX 文件）。我建议最好也列出所有的 CSS 和 图片文件，这样生成 Kindle 电子书时，任何不存在的文件（或拼写错误的文件）都会出现警告提示。
  - Spine：HTML 文件列表，按照它们被阅读的先后顺序排列。
  - Guide：这个元素指向你书中的关键项，比如 TOC（目录），以及在有致辞的情况下，正文的开始位置，等等。
4. 调用kindlgen生成mobi，并清理中间文件
```shell
/tools/mac/kindlegen /cache/book_name.opf
```
## 对应函数
1. make_html()
2. make_ncx()
3. make_opf()
4. make_mobi()

## 三方环境
Python包：jinja2；
Kindle官方转化工具：KindleGen
1. 利用kindle的官方文档解包出来的文件作为HTML和XML模板；
2. jinjia2调用这些模板后，输入小说信息对其进行渲染；
3. 保存渲染后文件至Cache；
4. 利用KindleGen官方工具将OPF文件转化为MOBI

## 使用方法一：调用函数
依次执行以下函数：
  1. make_html()
  2. make_ncx()
  3. make_opf()
  4. make_mobi()
  
## 使用方法二：测试执行函数
取消main注释，执行main.py，作为测试方法，测试原始信息在templates/test_source.py内

