from apps.user.models import EmailVerificationModel

from random import Random

from django.core.mail import send_mail

from mysite.settings import EMAIL_FROM


# 获取随机字符串
def get_random_string(code_length):
    string = ""
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(code_length):
        string += chars[random.randint(0, length)]
    return string


def Email_Send_Register(email,sendtype="register"):
    email_content = EmailVerificationModel()
    email_code = get_random_string(16)
    email_content.code = email_code
    email_content.email = email
    email_content.send_type = sendtype
    email_content.save()

    email_title = '用户注册'
    email_body = '点击此链接完成注册.http://127.0.0.1:8000/user/sign-up/activate/{0}'.format(email_code)
    send_key = send_mail(email_title, email_body, EMAIL_FROM, [email])


def Email_Send_Forget(email,sendtype="forget"):
    email_content = EmailVerificationModel()
    email_code = get_random_string(16)
    email_content.code = email_code
    email_content.email = email
    email_content.send_type = sendtype
    email_content.save()

    email_title = '密码找回'
    email_body = '点击此链接密码找回.http://127.0.0.1:8000/user/forget/verification/{0}'.format(email_code)
    send_key = send_mail(email_title, email_body, EMAIL_FROM, [email])
