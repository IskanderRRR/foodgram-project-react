from django.urls import include, path
from rest_framework import routers

from .views import (IngredientViewSet, RecipeViewSet, ShoppingCartViewSet,
                    TagViewSet)

router = routers.DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('recipes', ShoppingCartViewSet, basename='shopping_cart')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
