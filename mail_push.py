import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import formataddr

def mobi_push(from_mail,to_mail,book_dir):
    msg = MIMEMultipart()
    msg['Subject'] = 'Convert'
    msg['From'] = Header(from_mail,'utf-8')
    msg['To'] = Header(to_mail,'utf-8')
    book_name = book_dir.split('/')[-1]

    attach_mobi = MIMEApplication(open(book_dir,'rb').read())
    attach_mobi.add_header('content-disposition', 'attachment', filename=book_name)
    msg.attach(attach_mobi)

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(from_mail, [to_mail], msg.as_string())
        smtpObj.quit()
        print("邮件发送成功")
        return True
    except smtplib.SMTPException:
        print("Error: 发送邮件失败")
        print('注意：请将发送邮箱添加至Kindle认可邮箱列表')
        return False

def mobi_push_by_qqmail(from_account,to_mail,book_dir):
    my_sender = from_account['mail']
    my_pass = from_account['auth_code']
    my_user = to_mail

    msg = MIMEMultipart()
    msg['From'] = formataddr(["Kindle推送服务", my_sender])
    msg['To'] = formataddr(["Kindle", my_user])
    msg['Subject'] = "Convert"


    book_name = book_dir.split('/')[-1]
    attach_mobi = MIMEApplication(open(book_dir, 'rb').read())
    attach_mobi.add_header('content-disposition', 'attachment', filename=book_name)
    msg.attach(attach_mobi)

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        print("邮件发送成功")
        return True
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        print("Error:发送失败")
        print('注意：请将发送邮箱添加至Kindle认可邮箱列表')
        return False