from django.db import models

# Create your models here.


class Siteinfo(models.Model):
    id = models.AutoField(primary_key=True, default=0)
    title = models.CharField(max_length=64, default="图书置换平台")
    announcement = models.TextField(
        default="空", blank=True, null=True, verbose_name='公告')
    guide = models.TextField(default="空", blank=True,
                             null=True, verbose_name='指导')

    def __str__(self,):
        return str(self.id)+" | " + self.title


class BookCategory(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, default="默认类别")

    def __str__(self,):
        return str(self.id)+" | " + self.title
