from django.db import models


class User(models.Model):
    login = (
        (0, u'离线'),
        (1, u'在线'),
    )
    genders = (
        (0, u'男'),
        (1, u'女'),
    )
    username = models.CharField(verbose_name='用户名', max_length=128)
    email = models.EmailField(verbose_name='邮箱')
    password = models.CharField(verbose_name='密码', max_length=256)
    gender = models.IntegerField(verbose_name='性别', choices=genders, default=0)
    portrait = models.CharField(verbose_name='头像', max_length=256, default='/static/img/man.jpg')
    is_login = models.IntegerField(verbose_name='登录状态', choices=login, default=0)

    def __str__(self):
        return self.username
