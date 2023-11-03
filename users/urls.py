from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
)

from users import views

router = DefaultRouter()

router.register(r'', views.UserListView, 'users')


urlpatterns = [
    path('users/reg/', views.RegistrationView.as_view(), name='reg'),
    path('users/me/', views.MeView.as_view({'get': 'retrieve'}), name='me'),
]

urlpatterns += path('users/', include(router.urls)),
