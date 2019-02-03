from django.contrib import admin
from books.models import BooksInfo, MarkedBook, Orders, Address

# Register your models here.
admin.site.register(BooksInfo)
admin.site.register(MarkedBook)
admin.site.register(Orders)
admin.site.register(Address)
