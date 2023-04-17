from django.contrib import admin

from .models import Follow, User


class BaseAdminSettings(admin.ModelAdmin):
    """
    Базовая модель админки.
    """
    empty_value_display = '-пусто-'
    list_filter = ('email', 'username')


@admin.register(User)
class UsersAdmin(BaseAdminSettings):
    """
    Админка пользователя.
    """
    list_display = (
        'id',
        'role',
        'username',
        'email',
        'first_name',
        'last_name'
    )
    list_display_links = ('id', 'username')
    search_fields = ('role', 'username')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """
    Админка подписок.
    """
    list_display = (
        'id',
        'user',
        'author'
    )
    list_display_links = ('id', 'user')
    search_fields = ('user',)
