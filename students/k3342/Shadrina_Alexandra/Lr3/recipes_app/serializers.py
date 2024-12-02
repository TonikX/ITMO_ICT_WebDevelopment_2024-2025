from rest_framework import serializers
from .models import User, Recipe, Tag, RecipeTag, Comment, SavedRecipe, Subscription, Rating


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'date_joined']
        ref_name = 'CustomUserSerializer'


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'instructions',
            'complexity', 'author', 'image_urls',
            'video_url', 'average_rating', 'tags'
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class RecipeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeTag
        fields = ['id', 'recipe', 'tag']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    recipe = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'recipe', 'user', 'content', 'created_at']


class SavedRecipeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    recipe = serializers.StringRelatedField()

    class Meta:
        model = SavedRecipe
        fields = ['id', 'user', 'recipe']


class SubscriptionSerializer(serializers.ModelSerializer):
    subscriber = serializers.StringRelatedField()
    chef = serializers.StringRelatedField()

    class Meta:
        model = Subscription
        fields = ['id', 'subscriber', 'chef']


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    recipe = serializers.StringRelatedField()

    class Meta:
        model = Rating
        fields = ['id', 'recipe', 'user', 'rating_value']
