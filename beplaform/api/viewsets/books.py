from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
# from rest_framework.decorators import permission_classes as pc, authentication_classes as ac
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from api.serializers import BooksInfoSerializer, MarkedBookSerializer, AddressSerializer, OrdersSerializer, OrdersESerializer, OrdersASerializer
from books.models import BooksInfo, MarkedBook, Address, Orders
from rest_framework.authentication import BasicAuthentication
from util.permission import CsrfExemptSessionAuthentication as SessionAuthentication


class BooksInfoViewSet(ModelViewSet):
    serializer_class = BooksInfoSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post',
                         'update', 'delete', 'head', 'options', ]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('category', 'id', )
    search_fields = ('title',)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAuthenticated, ]
        return super(BooksInfoViewSet, self).get_permissions()

    def get_queryset(self):
        return BooksInfo.objects.all().values()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, ],)
    def mybooks(self, request):
        c = {
            'user': self.request.user,
        }
        if request.query_params.get('cid'):
            c['category_id'] = request.query_params.get('cid')
        return Response(BooksInfo.objects.filter(**c).values())

    def create(self, request):
        s = BooksInfoSerializer(data=request.data, many=False)
        s.is_valid(raise_exception=True)
        s.validated_data['user'] = self.request.user
        s.create(s.validated_data)
        return Response(status=201)


class MarkedBookViewSet(ModelViewSet):
    serializer_class = MarkedBookSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['get', 'post', 'delete', 'head', 'options', ]
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'book',)

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
    authentication_classes = (SessionAuthentication, BasicAuthentication)

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
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id',)

    def get_queryset(self,):
        return Orders.objects.filter(user=self.request.user).all()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, ])
    def tome(self, request):
        v = Orders.objects.filter(
            book__user_id=self.request.query_params.get('uid')).all().values()
        print(v)
        for vv in v:
            if vv.get('user_id'):
                a = Address.objects.filter(user_id=vv.get('user_id')).first()
                vv['user_address'] = a.address
        return Response(v)

    @action(detail=False, methods=['post'], serializer_class=OrdersASerializer, permission_classes=[IsAuthenticated, ])
    def start(self, request):
        s = OrdersASerializer(data=request.data, many=False)
        print("-------")
        s.is_valid(raise_exception=True)
        print("222-------")

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
