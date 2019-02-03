from books.models import BooksInfo, MarkedBook, Address, Orders
from siteinfo.models import Siteinfo, BookCategory
from rest_framework import serializers


class SiteinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Siteinfo
        exclude = ('id',)


class BookcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = '__all__'


class BooksInfoSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    category_name = serializers.ReadOnlyField(source='category.title')
    available = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()
    datetime = serializers.ReadOnlyField()

    def get_user_address(self, obj):
        a = Address.objects.filter(user=obj.user).first()
        if a == None:
            return ''
        return a.address

    user_address = serializers.SerializerMethodField()

    class Meta:
        model = BooksInfo
        fields = ("id", "wonder", "title", "author", "press", "isbn", "month", "boughtdate", 'category',
                  "price", "page", "quality", "datetime", "img", "available", "user_email", "category_name", 'user_address')


class MarkedBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = MarkedBook
        exclude = ('user',)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('user',)


class OrdersSerializer(serializers.ModelSerializer):
    def get_condition(self, obj):
        a = BooksInfo.objects.filter(id=obj.condition).first()
        if a == None:
            return ''
        s = BooksInfoSerializer(instance=a, many=False)
        # s.is_valid(raise_exception=False)
        return s.data

    condition = serializers.SerializerMethodField()
    status = serializers.ReadOnlyField()
    book = BooksInfoSerializer(many=False)

    class Meta:
        model = Orders
        fields = ('id', 'status', 'book', 'datetime', 'condition')


class OrdersESerializer(serializers.Serializer):

    order_id = serializers.IntegerField()

    class Meta:

        fields = ('order_id',)
