from django.db import models
from django.contrib.auth.models import User
from siteinfo.models import BookCategory


class BooksInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        BookCategory, null=True, on_delete=models.CASCADE)
    wonder = models.IntegerField(default=0)
    title = models.CharField(max_length=64)
    author = models.CharField(max_length=32, blank=True, null=True)
    press = models.CharField(max_length=64, blank=True, null=True)
    isbn = models.CharField(max_length=64, blank=True, null=True)
    month = models.DateField()
    boughtdate = models.DateField()
    price = models.FloatField(default=0.00)
    page = models.IntegerField(default=0)
    quality = models.IntegerField(default=3)
    datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    img = models.TextField(blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self,):
        return 'ID {} | 标题 {} | 价格 {} | 可换 {} | 发布时间 {}'.format(self.id, self.title, self.price, self.available, self.datetime)

    class Meta:
        permissions = (
            ('read_item', 'Can read item'),
        )


class MarkedBook(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(BooksInfo, on_delete=models.CASCADE)

    def __str__(self,):
        return 'ID {} | 标题 {} '.format(self.id, self.book.title)


class Address(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=384)

    def __str__(self,):
        return '地址 {}'.format(self.address)


class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(BooksInfo, on_delete=models.CASCADE)
    condition = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self,):
        a = BooksInfo.objects.filter(id=self.condition).first()
        return 'ID {} | 发起人email {} | 图书标题 {} | 交换书籍 {} | 交易成功 {} | 发起日期 {}'.format(self.id, self.user.email, self.book.title, a.title, self.status, self.datetime)
