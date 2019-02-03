from django.contrib.auth.models import User, Group
from django.contrib.auth.backends import ModelBackend as DjangoModelBackend
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewset(ViewSet):
    permission_classes = []

    def list(self, request):
        u = User.objects.filter(id=request.user.id).first()
        if u:
            return Response({
                'email': u.email,
            })
        return Response(status=403)

    def post(self, request):
        user = User.objects.create(
            username=request.data.get('email'),
            email=request.data.get('email'),
            is_staff=True,
        )
        user.set_password(str(request.data.get('password')))
        user.groups.add(Group.objects.filter(id=1).first())
        user.save()
        return Response({"status": "success", "response": "User Successfully Created"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post', ], )
    def login(self, request):
        print(request.data)
        user = DjangoModelBackend().authenticate(request, username=request.data.get(
            'email'), password=request.data.get('password'))
        if user != None:
            login(request, user)
            return Response({"status": True})
        else:
            return Response({"status": False})

    @action(detail=False, methods=['get', ], )
    def logout(self, request):
        logout(request)
        return Response({"status": True})
