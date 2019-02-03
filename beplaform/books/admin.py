from django.contrib import admin
from django.contrib.auth.models import User

from books.models import BooksInfo, MarkedBook, Orders, Address

# Register your models here.


class B(admin.ModelAdmin):
    def get_queryset(self, request):
        query = BooksInfo.objects.filter(user=request.user)
        if request.user.is_superuser:
            query = BooksInfo.objects.all()
        return query

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit choices for 'picture' field to only your pictures."""
        if db_field.name == 'user':
            if not request.user.is_superuser:
                kwargs["queryset"] = User.objects.filter(
                    id=request.user.id)
        return super(B, self).formfield_for_foreignkey(
            db_field, request, **kwargs)


class M(admin.ModelAdmin):
    def get_queryset(self, request):
        query = MarkedBook.objects.filter(user=request.user)
        if request.user.is_superuser:
            query = MarkedBook.objects.all()
        return query

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit choices for 'picture' field to only your pictures."""
        if db_field.name == 'user':
            if not request.user.is_superuser:
                kwargs["queryset"] = User.objects.filter(
                    id=request.user.id)
        return super(M, self).formfield_for_foreignkey(
            db_field, request, **kwargs)


class O(admin.ModelAdmin):
    def get_queryset(self, request):
        query = Orders.objects.filter(user=request.user)
        if request.user.is_superuser:
            query = Orders.objects.all()
        return query

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit choices for 'picture' field to only your pictures."""
        if db_field.name == 'user':
            if not request.user.is_superuser:
                kwargs["queryset"] = User.objects.filter(
                    id=request.user.id)
        return super(O, self).formfield_for_foreignkey(
            db_field, request, **kwargs)


class A(admin.ModelAdmin):
    def get_queryset(self, request):
        query = Address.objects.filter(user=request.user)
        if request.user.is_superuser:
            query = Address.objects.all()
        return query

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit choices for 'picture' field to only your pictures."""
        if db_field.name == 'user':
            if not request.user.is_superuser:
                kwargs["queryset"] = User.objects.filter(
                    id=request.user.id)
        return super(A, self).formfield_for_foreignkey(
            db_field, request, **kwargs)


admin.site.register(BooksInfo, B)
admin.site.register(MarkedBook, M)
admin.site.register(Orders, O)
admin.site.register(Address, A)
