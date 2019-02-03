from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from api.serializers import SiteinfoSerializer, BookcategorySerializer
from siteinfo.models import Siteinfo, BookCategory
from util.permission import IsSuperUser


# @method_decorator(csrf_exempt, name='dispatch')


class SiteinfoViewSet(ViewSet):
    def list(self, request):
        a = SiteinfoSerializer(Siteinfo.objects.first(), many=False)
        return Response(a.data)

    @action(detail=False, methods=['put'], permission_classes=[IsSuperUser, ])
    def update_site(self, request, pk=None):
        s = SiteinfoSerializer(data=request.data, many=False)
        s.is_valid(raise_exception=True)
        u = Siteinfo.objects.first()
        if u == None:
            s.create(s.validated_data)
        else:
            s.save(id=u.id)
        return Response(status=200)


class BookCategoryViewSet(ModelViewSet):
    queryset = BookCategory.objects.all()
    serializer_class = BookcategorySerializer

    def get_permissions(self):
        print(self.request.user.is_superuser)
        print(self.action)
        if self.action == "list" or self.request.user.is_superuser:
            permission_classes = []
        else:
            permission_classes = [IsSuperUser]
        return [permission() for permission in permission_classes]
