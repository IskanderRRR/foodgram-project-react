from django.contrib import admin

from users.models import Subscribe, User
from . import models
from .forms import TagForm


class IngredientToRecipeInLine(admin.StackedInline):
    model = models.IngredientToRecipe
    extra = 0


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'cooking_time', 'favorites']
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')
    readonly_fields = ('favorites',)
    filter_horizontal = ('tags',)
    inlines = [IngredientToRecipeInLine]

    def in_favorite(self, obj):
        return obj.in_favorite.all().count()

    in_favorite.short_description = 'Количество добавлений в избранное'


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    form = TagForm
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit']
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(models.IngredientToRecipe)
class IngredientToRecipeAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'ingredient', 'amount']
    list_filter = ('recipe', 'ingredient')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'password',
        'first_name',
        'last_name',
        'email',
        'is_subscribed'
    ]


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['user', 'author']


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe']
    list_filter = ('user', 'recipe')
    search_fields = ('user', 'recipe')


@admin.register(models.ShoppingCart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'user']
    list_filter = ('recipe', 'user')
    search_fields = ('user',)