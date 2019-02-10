# coding=utf-8
import jinja2
import os

env = jinja2.Environment(loader=jinja2.FileSystemLoader([r"templates/"]))
chapter_template = env.get_template('chapter_template.html')
toc_template = env.get_template("toc_template.html")
opf_template = env.get_template('opf.html')
ncx_template = env.get_template('ncx.html')


# 1. 每章节正文写入HTML文件，生成目录toc.html

def make_html(chapter_list, out_dir=None):
    # 输入章节列表，单个列表元素是字典类型，正文是列表
    # {'章节名': '第2章 7号记忆体',
    #  '正文': ['第一段内容'，'第二段内容'],
    #  }

    # 返回列表：[
    # {'id': 1, 'title': '第1章 我是谁', 'fileName': '1.html'},
    # {'id': 2, 'title': '第2章 7号记忆体', 'fileName': '2.html'},
    # {'id': 10, 'title': '第10章 神秘玩家', 'fileName': '10.html'}
    # ]
    html_files_list = []
    for id, chapter in enumerate(chapter_list):
        title = chapter["章节名"]
        context_list = chapter["正文"]
        html = chapter_template.render({'chapter_name': title, 'context': context_list})
        file_name = str(id + 1) + ".html"
        html_dir = "cache/" + file_name
        with open(html_dir,'w+') as fw:
            fw.write(html)
        print("正在生成%s"%file_name)
        dic = {
            "id":id + 1,
            "title":title,
            "fileName":file_name
        }
        html_files_list.append(dic)


    toc_html = toc_template.render({"navigation":html_files_list})
    with open("cache/toc.html",'w+') as fw:
        fw.write(toc_html)

    return html_files_list



# 2. 写入电子书目录导航：NCX

def make_ncx(book_name, book_contents):
    ncx_html = ncx_template.render({"book_name":book_name, "chapters":book_contents})
    # print(ncx_html)
    ncx_dir = "cache/" + "toc.ncx"
    with open(ncx_dir,'w+') as fw:
        fw.write(ncx_html)
    print("正在生成NCX文件......")

# 3. 写入电子书详情: OPF
def make_opf(bookInfo, file_list):
    opf_params = {
        'title':bookInfo["书名"],
        'author':bookInfo['作者'],
        'description':bookInfo['简介'],
        'navigation':file_list,
    }
    opf_html = opf_template.render(opf_params)

    opf_dir = "cache/" + bookInfo['书名'] + '.opf'
    print("正在生成OPF文件......")
    with open(opf_dir,'w+') as fw:
        fw.write(opf_html)
    return opf_dir

# 4. 调用kindlgen生成mobi
# 命令行：/Applications/kindlegen /Users/me/Documents/Book/book.opf
def make_mobi(opf_dir, kindleGen_dir=None):
    if kindleGen_dir == None:
        kindleGen_dir = 'tools/mac/kindlegen'
        os.system('%s %s -locale zh'%(kindleGen_dir,opf_dir))
        file_list = os.listdir("cache/")
        print("正在清理缓存......")
        mobi_file_name = ''
        for file in file_list:
            file_class = file.split('.')[-1]
            if file_class == 'mobi':
                mobi_file_name = file
                continue
            elif file_class == 'DS_Store':
                continue
            else:
                cache_file =  os.path.join('cache/',file)
                os.remove(cache_file)
        if os.path.isfile('cache/%s'%mobi_file_name) == True:
            print("Mobi文件生成成功！")
            return 'cache/%s'%mobi_file_name
        else:
            print("Mobi文件生成失败！")
            return False



# if __name__ == '__main__':
#     from templates.test_source import chapters,bookInfo
#
#     chap_list = make_html(chapters)
#     book_name = bookInfo['书名']
#     make_ncx(book_name, chap_list)
#     opf_dir = make_opf(bookInfo,chap_list)
#
#     book_dir = make_mobi(opf_dir)
#
#     from mail_push import mobi_push_by_qqmail
#
#     account = {
#         'mail':'邮箱账号',
#         'auth_code':'qq邮箱授权码'
#     }
#     receive_mail = 'kindle收件邮箱'
#     mobi_push_by_qqmail(account,receive_mail,book_dir)
#
