from django.contrib import admin

from chat.models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time')
    search_fields = ('id',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'text', 'timestamp')
    list_filter = ('conversation', 'sender')
    autocomplete_fields = ('conversation', 'sender')


