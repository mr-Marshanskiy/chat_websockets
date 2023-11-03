from django.contrib.auth import get_user_model
from django.db import models

from config import settings

User = settings.AUTH_USER_MODEL


class Conversation(models.Model):
    initiator = models.ForeignKey(
        User, models.SET_NULL, 'conversation_initiators', null=True,
    )
    receiver = models.ForeignKey(
        User, models.SET_NULL, 'conversation_receivers', null=True,
    )
    start_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, models.CASCADE, 'messages',
    )
    sender = models.ForeignKey(
        User, models.SET_NULL, 'message_senders', null=True,
    )
    text = models.CharField(max_length=200, blank=True)
    attachment = models.FileField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
