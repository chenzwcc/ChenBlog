# coding=utf8
from random import Random
from django.core.mail import send_mail
from users.models import EmailVerfyRecode
from ChenBlog.settings import EMAIL_FROM


# 生成随机字符串

def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email,host, send_type='register'):
    email_record = EmailVerfyRecode()
    # 将给用户发的信息保存在数据库中
    code = random_str(8)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    # c初始化为空
    email_title = ''
    email_body = ''

    if send_type == "register":
        email_title = "陈政伟博客注册激活链接"
        email_body = "请点击下面的链接激活你的账号:{0}/active/{1}".format(host,code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == "forgetpwd":
        email_title = "陈政伟博客密码重置链接"
        email_body = "请点击下面的链接重置你的密码:{0}/reset/{1}".format(host,code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
