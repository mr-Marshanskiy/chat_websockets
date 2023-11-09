from django.contrib import admin

from chat.models import Chat, Message, UserChat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('id', 'name',)


@admin.register(UserChat)
class UserChatAdmin(admin.ModelAdmin):
    readonly_fields = ('last_seen',)
    list_display = ('id', 'user', 'chat', 'last_seen',)
    search_fields = ('id', 'user_id', 'chat_id')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'text', 'timestamp')
    list_filter = ('chat', 'sender')
    autocomplete_fields = ('chat', 'sender')


