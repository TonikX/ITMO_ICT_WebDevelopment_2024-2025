from djoser import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, \
    CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Recipe, Comment, CuratedList, Like
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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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
        values = Like.objects.filter(user=self.request.user, status=True).select_related('recipe')
        recipes = [like.recipe for like in values]
        return recipes

class RecipeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        recipe = super().get_object()

        if self.request.method in ['PATCH', 'DELETE']:
            if recipe.author != self.request.user:
                raise PermissionDenied("You do not have permission to modify this recipe.")

        return recipe


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
