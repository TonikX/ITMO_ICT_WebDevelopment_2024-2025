from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers

from .models import User, Movie, Friend, Activity, List, ListMovie, Rating, Profile


class CustomUserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'password', 'avatar_url', 'created_at')
        extra_kwargs = {'password': {'write_only': True}}


class CustomUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id', 'username', 'email', 'avatar_url', 'created_at']


class FriendSerializer(serializers.ModelSerializer):
    friend_details = serializers.SerializerMethodField()

    class Meta:
        model = Friend
        fields = ['id', 'friend', 'friend_details']

    def get_friend_details(self, obj):
        return {
            'id': obj.friend.id,
            'email': obj.friend.email,
            'avatar_url': obj.friend.avatar_url,
            'username': obj.friend.username,
        }


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'movie', 'rating', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        user = validated_data['user']
        movie = validated_data['movie']
        rating, created = Rating.objects.update_or_create(
            user=user,
            movie=movie,
            defaults={'rating': validated_data['rating']}
        )
        return rating


# Activity Serializer
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'user', 'activity_type', 'activity_details', 'created_at']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'avatar_url', 'favorite_movies']


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "poster_url", "year", "genres", "rating"]


class ListMovieSerializer(serializers.ModelSerializer):
    movie_details = MovieSerializer(source="movie", read_only=True)

    class Meta:
        model = ListMovie
        fields = ["id", "movie_details"]


class ListSerializer(serializers.ModelSerializer):
    list_movies = ListMovieSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = ["id", "name", "list_movies", "created_at"]


class PublicMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "poster_url", "year", "genres", "rating"]


class PublicListMovieSerializer(serializers.ModelSerializer):
    movie_details = PublicMovieSerializer(source="movie", read_only=True)

    class Meta:
        model = ListMovie
        fields = ["id", "movie_details"]


class ListCreateSerializer(serializers.ModelSerializer):


    class Meta:
        model = List
        fields = ["id", "name", "created_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
