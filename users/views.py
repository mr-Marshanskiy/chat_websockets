from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from common.views import ListViewSet, RetrieveViewSet
from .serializers import UserSerializer, RegistrationSerializer


User = get_user_model()


@extend_schema_view(
    post=extend_schema(summary='User registration', tags=['Users']),
)
class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer


@extend_schema_view(
    list=extend_schema(summary='List users', tags=['Users']),
)
class UserListView(ListViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (
        SearchFilter,
    )
    search_fields = ('last_name', 'email', 'username',)


@extend_schema_view(
    retrieve=extend_schema(summary='Me', tags=['Users']),
)
class MeView(RetrieveViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
