from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chat import views


router = DefaultRouter()

router.register(r'(?P<pk>\d+)/messages', views.MessageView)
router.register('', views.ChatView)


urlpatterns = [
]

urlpatterns += path('chats/', include(router.urls)),
