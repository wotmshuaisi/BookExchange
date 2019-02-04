from books.models import BooksInfo, MarkedBook, Address, Orders
from siteinfo.models import Siteinfo, BookCategory
from rest_framework import serializers
from django.contrib.auth.models import User


class SiteinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Siteinfo
        exclude = ('id',)


class BookcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = '__all__'


class BooksInfoSerializer(serializers.ModelSerializer):
    available = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()
    datetime = serializers.ReadOnlyField()

    def get_user_address(self, obj):
        a = Address.objects.filter(user_id=obj['user_id']).first()
        if a == None:
            return ''
        return a.address

    def get_category_name(self, obj):
        a = BookCategory.objects.filter(
            id=obj['category_id']).first()
        if a == None:
            return ''
        return a.title

    def get_user_email(self, obj):
        a = User.objects.filter(id=obj['user_id']).first()
        if a == None:
            return ''
        return a.email

    category_name = serializers.SerializerMethodField()
    user_address = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = BooksInfo
        fields = ("id", "wonder", "title", "author", "press", "isbn", "month", "boughtdate", 'category_id', 'category', 'category_name',
                  "price", "page", "quality", "datetime", "img", "available", "user_id", 'user_email', 'user_address')


class MarkedBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = MarkedBook
        exclude = ('user',)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('user',)


class OrdersSerializer(serializers.ModelSerializer):
    # def get_condition(self, obj):
    #     a = BooksInfo.objects.filter(id=obj.condition).first()
    #     if a == None:
    #         return ''
    #     s = BooksInfoSerializer(instance=a, many=False)
    #     return s.data

    # bookemail = serializers.
    status = serializers.ReadOnlyField()
    # book = BooksInfoSerializer(many=False)

    class Meta:
        model = Orders
        fields = ('id', 'status', 'book', 'datetime', 'condition')


class OrdersASerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ('book', 'condition')


class OrdersESerializer(serializers.Serializer):

    order_id = serializers.IntegerField()

    class Meta:

        fields = ('order_id',)
