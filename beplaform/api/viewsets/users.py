from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response


class UserViewset(ViewSet):

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
        user.save()
        return Response({"status": "success", "response": "User Successfully Created"}, status=status.HTTP_201_CREATED)
