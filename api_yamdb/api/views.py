from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdmin
from .serializers import UsersSerializer
from users.models import CustomUser


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    queryset = CustomUser.objects.all()
    search_fields = ('username',)

    @action(detail=False, methods=('get', 'patch',),
            url_path='me', url_name='me',
            permission_classes=(IsAuthenticated,)
        )
    def get_me(self, request):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(role=instance.role)
                return Response(serializer.data)
        return Response(serializer.data)