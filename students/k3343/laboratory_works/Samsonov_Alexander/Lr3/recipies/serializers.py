from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Recipe, Ingredients, Comment, CuratedList


class RecipeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'header', 'thumbnail_link']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ['ingredient_name', 'quantity_si', 'unit_si']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class TagSerializer(serializers.Serializer):
    tag_name = serializers.CharField()

    def to_representation(self, instance):
        return instance.tag_name


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, allow_null=True)
    class Meta:
        model = Comment
        fields = [
            'id',
            'rating',
            'header',
            'content_text',
            'author'
        ]

    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Rating must be between 1 and 10.")
        return value


class RecipeDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'author',  # We're manually controlling the output here
            'header',
            'thumbnail_link',
            'content_json',
            'time_takes',
            'difficulty',
            'dt_update',
            'stars_sum',
            'number_ratings',
            'tags',
            'ingredients'
        ]
        depth = 1


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)  # Allow nested ingredient data

    class Meta:
        model = Recipe
        fields = [
            'header',
            'thumbnail_link',
            'content_json',
            'time_takes',
            'difficulty',
            'tags',
            'ingredients'
        ]

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            if 'id' in ingredient_data:
                ingredient = Ingredients.objects.get(id=ingredient_data['id'])
            else:
                ingredient = Ingredients.objects.create(**ingredient_data)

            recipe.ingredients.add(ingredient)

        recipe.tags.set(tags_data)

        return recipe


class CuratedListSerializer(serializers.ModelSerializer):
    recipes = RecipeListSerializer(many=True)
    class Meta:
        model = CuratedList
        fields = [
            'id',
            'header',
            'recipes'
        ]


class CuratedListDetailSerializer(serializers.ModelSerializer):
    recipes = RecipeListSerializer(many=True)
    Curator = UserSerializer()
    class Meta:
        model = CuratedList
        fields = "__all__"
