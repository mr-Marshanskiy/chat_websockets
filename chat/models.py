from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Chat(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, models.SET_NULL, 'created_chats', null=True,
    )

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chat'

    def __str__(self):
        return f'{self.name} {self.created_at}'


class UserChat(models.Model):
    chat = models.ForeignKey(
        Chat, models.CASCADE, 'users',
    )
    user = models.ForeignKey(
        User, models.CASCADE, 'chats',
    )
    last_seen = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User chat'
        verbose_name_plural = 'User chats'


class Message(models.Model):
    chat = models.ForeignKey(
        Chat, models.CASCADE, 'messages',
    )
    sender = models.ForeignKey(
        User, models.SET_NULL, 'message_senders', null=True,
    )
    text = models.CharField(max_length=200, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
