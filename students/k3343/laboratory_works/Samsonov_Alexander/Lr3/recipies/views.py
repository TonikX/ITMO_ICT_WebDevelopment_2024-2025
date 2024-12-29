from djoser import serializers
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Recipe, Comment, CuratedList, Like, Tags, Ingredients
from .serializers import RecipeListSerializer, RecipeDetailSerializer, RecipeCreateSerializer, CommentSerializer, \
    CuratedListSerializer, CuratedListDetailSerializer


class RecipeListCreateView(ListCreateAPIView):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = RecipeListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecipeCreateSerializer
        return RecipeListSerializer

    def create(self, validated_data, **kwargs):

        data = validated_data.data
        ingredients_data = data.pop('ingredients', [])
        tags = data.pop('tags', [])
        recipe = Recipe.objects.create(**data, author=self.request.user)

        for ingredient_data in ingredients_data:
            if 'id' in ingredient_data:
                ingredient = Ingredients.objects.get(id=ingredient_data['id'])
            else:
                ingredient = Ingredients.objects.get_or_create(**ingredient_data)[0]
            recipe.ingredients.add(ingredient)

        tags = [Tags.objects.get_or_create(tag_name=i)[0] for i in tags]
        recipe.tags.add(*tags)
        return Response({}, 200)

class MyRecipes(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeDetailSerializer

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)


class Toggle(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        obj, created = Like.objects.get_or_create(recipe=recipe, user=request.user)
        return Response({'liked': obj.status}, status=200)

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        obj, created = Like.objects.get_or_create(recipe=recipe, user=request.user)
        obj.status = not obj.status
        obj.save()
        return Response('Ok', status=200)


class MyLikedRecipes(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeDetailSerializer

    def get_queryset(self):
        return Recipe.objects.filter(
            like__user=self.request.user,
            like__status=True
        ).distinct()


class RecipeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == ['PATCH', 'PUT']:
            return RecipeCreateSerializer
        return RecipeDetailSerializer

    def get_object(self):
        recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])

        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if recipe.author != self.request.user:
                raise PermissionDenied("You do not have permission to modify this recipe.")

        return recipe

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.tags.clear()
        instance.ingredients.clear()
        instance.like_set.clear()
        instance.comment_set.clear()
        instance.save()

        self.perform_destroy(instance)
        return Response({'detail': 'Recipe deleted successfully.'}, status=200)


    def perform_destroy(self, instance):
        instance.delete()

class CanEdit(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if self.request.user.is_anonymous:
            return Response(False, status=200)
        if self.request.user == recipe.author:
            return Response(True, status=200)
        return Response(False, status=200)


class CommentListCreateView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        recipe_id = self.request.query_params.get('recipe_id', None)

        if recipe_id:
            return Comment.objects.filter(recipe__id=recipe_id)

        return Comment.objects.all()

    def perform_create(self, serializer):
        recipe_id = self.request.query_params.get('recipe_id')
        if not recipe_id:
            raise serializers.ValidationError({"recipe_id": "This field is required."})
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            raise serializers.ValidationError({"recipe_id": "Recipe not found."})

        serializer.save(author=self.request.user, recipe=recipe)


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to edit this comment.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to delete this comment.")
        instance.delete()


class CuratedListView(ListAPIView):
    queryset = CuratedList.objects.all()
    serializer_class = CuratedListSerializer


class CuratedListDetailedView(RetrieveAPIView):
    queryset = CuratedList.objects.all()
    serializer_class = CuratedListDetailSerializer
