from django.db.models import  F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.viewsets import GenericViewSet
from rest_framework import status


from recipes.models import (Favorite, Ingredient, Recipe, ShoppingCart, Tag,
                            IngredientToRecipe)
from .filters import IngredientSearchFilter, RecipeFilter
from .paginations import (RecipePageNumberPagination,
                          ShoppingCartPageNumberPagination)
from .permissions import OwnerOrReadOnly
from .serializers import (IngredientSerializer, RecipeFavoriteSerializer,
                          RecipeReadSerializer, RecipeWriteSerializer,
                          TagSerializer, ShoppingCartSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientSearchFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = RecipePageNumberPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add_favorite(self, request, recipe):
        Favorite.objects.get_or_create(user=request.user, recipe=recipe) 
        serializer = RecipeFavoriteSerializer(recipe)
        return Response(
            serializer.data,
            status=HTTP_201_CREATED,
        )

    def delete_favorite(self, request, recipe):
        favorite = Favorite.objects.filter(user=request.user, recipe=recipe)
        if not favorite.exists():
            return Response(
                {'errors': 'Этот рецепт не находится в избранных'},
                status=HTTP_400_BAD_REQUEST,
            )
        favorite.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        methods=('post', 'delete',),
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            return self.add_favorite(request, recipe)
        return self.delete_favorite(request, recipe)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        INGREDIENT = 'ingredient__name'
        UNIT = 'ingredient__measurement_unit'
        FILENAME = 'shopping_cart.txt'
        recipes = IngredientToRecipe.objects.filter(
            recipe__shoppingcart__user=request.user)
        ingredients = recipes.values(INGREDIENT, UNIT).annotate(
            total=Sum('ingredient__ingredient_recipe__amount'))
        content = ''
        for ingredient in ingredients:
            content += (
                f'{ingredient[INGREDIENT]}'
                f' ({ingredient[UNIT]})'
                f' — {ingredient["total"]}\r\n'
                )
        response = HttpResponse(
            content, content_type='text/plain,charset=utf8'
        )
        response['Content-Disposition'] = f'attachment; filename={FILENAME}'
        return response


class ShoppingCartViewSet(GenericViewSet):
    pagination_class = ShoppingCartPageNumberPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeFavoriteSerializer
    queryset = ShoppingCart.objects.all()
    http_method_names = ('post', 'delete',)
    
    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_instance = get_object_or_404(model, user=user, recipe=recipe)
        model_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def shopping_cart(self, request, pk):
        return self.post_method_for_actions(
            request, pk, serializers=ShoppingCartSerializer
        )
    
    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=ShoppingCart)
