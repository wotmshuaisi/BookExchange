from django.db.models import Q
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api.serializers import BooksInfoSerializer, MarkedBookSerializer, AddressSerializer, OrdersSerializer, OrdersESerializer
from util.permission import IsSuperUser
from books.models import BooksInfo, MarkedBook, Address, Orders


class BooksInfoViewSet(ModelViewSet):
    serializer_class = BooksInfoSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post',
                         'update', 'delete', 'head', 'options', ]

    def get_queryset(self,):
        return BooksInfo.objects.filter(user=self.request.user).all()

    def create(self, request):
        s = BooksInfoSerializer(data=request.data, many=False)
        s.is_valid(raise_exception=True)
        s.validated_data['user'] = self.request.user
        s.create(s.validated_data)
        return Response(status=201)


class MarkedBookViewSet(ModelViewSet):
    serializer_class = MarkedBookSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'head', 'options', ]

    def get_queryset(self,):
        return MarkedBook.objects.filter(user=self.request.user).all()

    def create(self, request):
        s = MarkedBookSerializer(data=request.data, many=False)
        s.is_valid(raise_exception=True)
        s.validated_data['user_id'] = self.request.user.id
        s.create(s.validated_data)
        return Response(status=201)


class AddressViewSet(ViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'head', 'options', ]

    def list(self, request):
        return Response(AddressSerializer(Address.objects.filter(user=request.user).first(), many=False).data)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated, ])
    def update_address(self, request, pk=None):
        s = AddressSerializer(data=request.data, many=False)
        s.is_valid(raise_exception=True)
        u = Address.objects.filter(user=request.user).first()
        if u == None:
            s.create(s.validated_data)
        else:
            s.save(address=u.address)
        return Response(status=200)


class OrdersViewSet(ModelViewSet):
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'head', 'options', ]

    def get_queryset(self,):
        return Orders.objects.filter(Q(user=self.request.user) | Q(book__user=self.request.user)).all()

    def create(self, request):
        s = OrdersSerializer(data=request.data, many=False)
        s.is_valid(raise_exception=True)

        condition = BooksInfo.objects.filter(user=self.request.user,
                                             id=s.validated_data.get('condition')).first()

        # exchanged
        if s.validated_data.get('book').available == False or condition.available == False:
            return Response(status=410)

        # conditoon not exists
        if condition == None:
            return Response(status=404)

        # user can not exchange his own books
        if request.user.id == s.validated_data.get('book').user.id:
            return Response(status=400)

        # user cannot use currently use to exchanging book to exchange other books
        if Orders.objects.filter(user=self.request.user, book=s.validated_data.get('book')).count() >= 1 or \
            Orders.objects.filter(user=self.request.user,
                                  condition=s.validated_data.get('condition')).count() >= 1:
            return Response(status=409)

        # exchanging must fit in category
        if condition.category.id != s.validated_data.get('book').wonder:
            return Response(status=406)

        s.validated_data['user'] = self.request.user
        s.create(s.validated_data)
        return Response(status=201)

    def destroy(self, request, pk=None):
        q = Orders.objects.filter(
            id=pk, status=False, user=self.request.user).first()
        if q == None:
            return Response(status=400)
        q.delete()
        return Response(status=202)

    @action(detail=False, methods=['post'], serializer_class=OrdersESerializer, permission_classes=[IsAuthenticated, ])
    def exchange(self, request):
        s = OrdersESerializer(data=request.data, many=False)
        s.is_valid(raise_exception=True)
        q = Orders.objects.filter(
            book__user=self.request.user, id=s.validated_data.get('order_id')).first()

        if q == None:
            return Response(status=404)

        condition = BooksInfo.objects.filter(id=q.condition).first()
        target = BooksInfo.objects.filter(id=q.book.id).first()
        # exchanged
        if q.book.available == False or condition.available == False:
            return Response(status=410)

        target.available = False
        target.save()
        condition.available = False
        condition.save()

        Orders.objects.filter(book__user=self.request.user,
                              id=s.validated_data.get('order_id')).update(status=True)
        return Response(status=200)
