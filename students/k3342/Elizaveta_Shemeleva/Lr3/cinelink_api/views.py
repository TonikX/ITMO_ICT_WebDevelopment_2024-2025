from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import MovieFilter
from .models import User, Movie, Friend, List, ListMovie, Rating, Activity, Profile
from .serializers import (
    CustomUserSerializer, MovieSerializer, FriendSerializer, ListMovieSerializer,
    RatingSerializer, ActivitySerializer, ListCreateSerializer, ListSerializer
)


class FriendDetailView(APIView):
    """
    Представление для получения детальной информации о друге, включая список любимых фильмов и статус дружбы.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, friend_id):
        """
        Возвращает данные о друге, список любимых фильмов и статус дружбы.

        :param request: HTTP-запрос.
        :param friend_id: Идентификатор друга.
        :return: Данные о друге и его любимых фильмах.
        """
        friend = get_object_or_404(User, id=friend_id)
        profile = Profile.objects.filter(user=friend).first()
        if not profile:
            profile = Profile.objects.create(user=friend, username=friend.username)

        favorite_movies_ids = profile.favorite_movies.split(",") if profile.favorite_movies else []
        favorite_movies = Movie.objects.filter(id__in=favorite_movies_ids)
        favorite_movies_serialized = MovieSerializer(favorite_movies, many=True).data

        # is_friend = request.user.friends.filter(id=friend.id).exists()
        is_friend = Friend.objects.filter(
            Q(user=request.user, friend=friend) | Q(user=friend, friend=request.user)
        ).exists()

        friend_data = {
            "id": friend.id,
            "username": friend.username,
            "email": friend.email,
            "avatar_url": profile.avatar_url,
        }

        return Response({
            "friend": friend_data,
            "favorite_movies": favorite_movies_serialized,
            "is_friend": is_friend,
        })


class RateMovieView(APIView):
    """
    Представление для выставления или обновления оценки фильма аутентифицированным пользователем.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Выставляет или обновляет оценку фильму.

        :param request: HTTP-запрос, содержащий поля 'movie' и 'rating'.
        :return: Данные об установленной оценке.
        """
        movie_id = request.data.get("movie")
        rating_value = request.data.get("rating")

        if not movie_id or not rating_value:
            return Response({"error": "Необходимы идентификатор фильма и оценка."}, status=status.HTTP_400_BAD_REQUEST)

        if not (1 <= int(rating_value) <= 10):
            return Response({"error": "Оценка должна быть в диапазоне от 1 до 10."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({"error": "Фильм не найден."}, status=status.HTTP_404_NOT_FOUND)

        rating, created = Rating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={"rating": rating_value}
        )

        response_data = {
            "id": rating.id,
            "user": rating.user.id,
            "movie": rating.movie.id,
            "rating": rating.rating,
            "created_at": rating.created_at
        }

        if created:
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(response_data, status=status.HTTP_200_OK)


class ToggleFriendshipView(APIView):
    """
    Представление для добавления или удаления друга у текущего пользователя.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, friend_id):
        """
        Добавляет или удаляет друга по идентификатору.

        :param request: HTTP-запрос.
        :param friend_id: Идентификатор пользователя, которого добавляют или удаляют из друзей.
        :return: Сообщение об изменении статуса дружбы.
        """
        friend = get_object_or_404(User, id=friend_id)

        if friend == request.user:
            return Response(
                {"error": "Нельзя добавить себя в друзья."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        existing_friendship = Friend.objects.filter(user=request.user, friend=friend)

        if existing_friendship.exists():
            existing_friendship.delete()
            return Response({"is_friend": False, "message": "Друг успешно удалён."}, status=status.HTTP_200_OK)

        Friend.objects.create(user=request.user, friend=friend)
        return Response({"is_friend": True, "message": "Друг успешно добавлен."}, status=status.HTTP_201_CREATED)


class TopMoviesView(APIView):
    """
    Представление для получения списка топ-5 фильмов по рейтингу.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Возвращает список из 5 фильмов с наивысшим рейтингом.

        :param request: HTTP-запрос.
        :return: Сериализованные данные фильмов.
        """
        top_movies = Movie.objects.order_by('-rating')[:5]
        serializer = MovieSerializer(top_movies, many=True)
        return Response(serializer.data)


class ProfileView(APIView):
    """
    Представление для получения и обновления профиля аутентифицированного пользователя.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Возвращает данные профиля текущего пользователя.

        :param request: HTTP-запрос.
        :return: Информация о профиле и список любимых фильмов.
        """
        user = request.user
        profile, _ = Profile.objects.get_or_create(user=user)

        profile_data = {
            "username": profile.username,
            "avatar_url": profile.avatar_url,
            "favorites": profile.favorite_movies.split(", ") if profile.favorite_movies else [],
        }
        return Response(profile_data)

    def put(self, request):
        user = request.user
        data = request.data

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.username = data.get("username", profile.username)
        profile.avatar_url = data.get("avatar_url", profile.avatar_url)
        profile.favorite_movies = ", ".join(data.get("favorites", []))
        profile.save()

        updated = False

        if profile.username and user.username != profile.username:
            user.username = profile.username
            updated = True

        if profile.avatar_url and hasattr(user, "profile") and user.profile.avatar_url != profile.avatar_url:
            user.profile.avatar_url = profile.avatar_url
            updated = True

        if updated:
            user.save()

        return Response({"message": "Профиль успешно обновлён!"}, status=200)


class PublicFavoritesView(APIView):
    """
    Публичное представление для получения списка любимых фильмов пользователя по его идентификатору.
    """

    permission_classes = [AllowAny]

    def get(self, request, user_id):
        """
        Возвращает список любимых фильмов указанного пользователя.

        :param request: HTTP-запрос.
        :param user_id: Идентификатор пользователя.
        :return: Сериализованные данные любимых фильмов.
        """
        try:
            profile = Profile.objects.filter(user_id=user_id).first()
            if not profile or not profile.favorite_movies:
                return Response([], status=200)

            favorite_movie_ids = profile.favorite_movies.split(", ")
            movies = Movie.objects.filter(id__in=favorite_movie_ids)
            serializer = MovieSerializer(movies, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class FriendsActivityView(APIView):
    """
    Представление для получения списка последних оценок фильмов, выставленных друзьями текущего пользователя.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Возвращает недавнюю активность (оценки) друзей пользователя, отсортированную по дате создания.

        :param request: HTTP-запрос.
        :return: Сериализованные данные о деятельности (оценках) друзей.
        """
        user = request.user
        friends = Friend.objects.filter(user=user).values_list('friend', flat=True)
        activities = Rating.objects.filter(user_id__in=friends).order_by('-created_at')

        serialized_data = [
            {
                "id": activity.id,
                "user": {
                    "id": activity.user.id,
                    "username": activity.user.username,
                },
                "movie": {
                    "id": activity.movie.id,
                    "title": activity.movie.title,
                    "poster_url": activity.movie.poster_url,
                },
                "rating": activity.rating,
                "created_at": activity.created_at,
            }
            for activity in activities
        ]

        return Response(serialized_data, status=200)


class FriendsListView(APIView):
    """
    Представление для получения списка друзей по идентификатору пользователя.
    """

    permission_classes = [AllowAny]

    def get(self, request, user_id):
        """
        Возвращает список друзей для указанного пользователя.

        :param request: HTTP-запрос.
        :param user_id: Идентификатор пользователя.
        :return: Сериализованные данные пользователей (друзей).
        """
        user = get_object_or_404(User, id=user_id)
        friends = Friend.objects.filter(user=user).select_related("friend")
        serialized_friends = CustomUserSerializer([f.friend for f in friends], many=True)
        return Response(serialized_friends.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления пользователями.
    """

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class UserSearchView(APIView):
    """
    Представление для поиска пользователей по имени или email (частичное совпадение).
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Возвращает список пользователей, чьи имена или email содержат переданную подстроку.

        :param request: HTTP-запрос с параметром 'search'.
        :return: Сериализованные данные соответствующих пользователей.
        """
        query = request.query_params.get("search", "").strip()
        if not query:
            return Response([], status=status.HTTP_200_OK)

        users = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        ).exclude(username__isnull=True)[:20]
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserListMoviesView(APIView):
    """
    Представление для получения фильмов, связанных с определённым списком, принадлежащим аутентифицированному пользователю.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, list_id):
        """
        Возвращает фильмы, находящиеся в указанном списке аутентифицированного пользователя.

        :param request: HTTP-запрос.
        :param list_id: Идентификатор списка.
        :return: Сериализованные данные о фильмах, входящих в список.
        """
        user = request.user
        try:
            user_list = List.objects.get(id=list_id, user=user)
        except List.DoesNotExist:
            return Response(
                {"error": "Список не найден или нет прав на просмотр этого списка."},
                status=status.HTTP_404_NOT_FOUND
            )

        list_movies = ListMovie.objects.filter(list=user_list)
        serializer = ListMovieSerializer(list_movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieSearchView(APIView):
    """
    Представление для поиска фильмов по названию, жанрам или году.
    """

    def get(self, request):
        """
        Возвращает фильмы, удовлетворяющие поисковому запросу (по названию, жанрам или году).

        :param request: HTTP-запрос с параметром 'search'.
        :return: Сериализованные данные соответствующих фильмов.
        """
        query = request.query_params.get("search", "").strip()
        if not query:
            return Response({"detail": "Требуется строка поиска."}, status=status.HTTP_400_BAD_REQUEST)

        movies = Movie.objects.filter(
            Q(title__icontains=query) | Q(genres__icontains=query) | Q(year__icontains=query)
        )[:20]
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieViewSet(ModelViewSet):
    """
    ViewSet для управления фильмами, с возможностью фильтрации и сортировки.
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MovieFilter
    ordering_fields = ["title", "year", "rating"]
    ordering = ["title"]

    def get_object(self):
        """
        Переопределение для получения объекта фильма по его ID.
        """
        return super().get_object()

    @action(detail=False, methods=["get"])
    def filters(self, request):
        """
        Возвращает доступные варианты фильтров для фильмов (жанры, десятилетия, рейтинги).

        :param request: HTTP-запрос.
        :return: Жанры, десятилетия и рейтинги.
        """
        genres = Movie.objects.values_list("genres", flat=True).distinct()
        decades = [
            f"{year}s"
            for year in range(1900, 2030, 10)
            if Movie.objects.filter(year__gte=year, year__lt=year + 10).exists()
        ]
        ratings = Movie.objects.values_list("rating", flat=True).distinct()

        genre_set = set()
        for genre_list in genres:
            genre_set.update(genre_list.split(", "))

        return Response({
            "genres": sorted(genre_set),
            "decades": decades,
            "ratings": sorted(set(ratings)),
        })

    @action(detail=True, methods=["get"], url_path="details", url_name="movie-details")
    def details(self, request, pk=None):
        """
        Возвращает детальную информацию о фильме по его ID.

        :param request: HTTP-запрос.
        :param pk: Идентификатор фильма.
        :return: Сериализованные данные фильма.
        """
        try:
            movie = self.get_object()
            serializer = self.get_serializer(movie)
            return Response(serializer.data)
        except Movie.DoesNotExist:
            return Response({"error": "Фильм не найден."}, status=404)


class FriendViewSet(ReadOnlyModelViewSet):
    """
    ReadOnlyModelViewSet для отношений друзей (Friend).
    """

    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает список друзей для пользователя, чей ID передан в URL.

        :return: QuerySet с объектами Friend.
        """
        user_id = self.kwargs.get('user_id')
        return Friend.objects.filter(user_id=user_id)


class ListViewSet(viewsets.ModelViewSet):
    """
    ViewSet для создания, получения, обновления и удаления списков (List).
    """

    queryset = List.objects.all()
    serializer_class = ListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Фильтрует списки по текущему аутентифицированному пользователю.

        :return: QuerySet со списками пользователя.
        """
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """
        Определяет, какой сериализатор использовать в зависимости от действия.

        :return: Класс сериализатора.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return ListCreateSerializer
        return ListSerializer

    def perform_create(self, serializer):
        """
        Ассоциирует создаваемый список с аутентифицированным пользователем.

        :param serializer: Экземпляр сериализатора.
        """
        serializer.save()

    @action(detail=True, methods=['post'], url_path='movies')
    def add_movie(self, request, pk=None):
        """
        Добавляет фильм в указанный список.

        :param request: HTTP-запрос с полем 'movie_id'.
        :param pk: Идентификатор списка.
        :return: Сообщение об успешном добавлении фильма.
        """
        try:
            list_instance = self.get_object()
            movie_id = request.data.get('movie_id')
            if not movie_id:
                return Response({"error": "Необходимо указать ID фильма."}, status=status.HTTP_400_BAD_REQUEST)

            movie = Movie.objects.filter(id=movie_id).first()
            if not movie:
                return Response({"error": "Фильм не найден."}, status=status.HTTP_404_NOT_FOUND)

            ListMovie.objects.create(list=list_instance, movie=movie)
            return Response({"message": "Фильм успешно добавлен в список."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListMovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления связями между списками и фильмами (ListMovie).
    """

    queryset = ListMovie.objects.all()
    serializer_class = ListMovieSerializer


class RatingViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления оценками (Rating).
    """

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class MovieRatingView(APIView):
    """
    Представление для получения оценки фильма текущим аутентифицированным пользователем.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id):
        """
        Возвращает оценку фильма текущим пользователем, если она существует.

        :param request: HTTP-запрос.
        :param movie_id: Идентификатор фильма.
        :return: Оценка пользователя или None, если оценки нет.
        """
        try:
            movie = Movie.objects.get(id=movie_id)
            rating = Rating.objects.filter(user=request.user, movie=movie).first()
            if rating:
                return Response({"rating": rating.rating}, status=status.HTTP_200_OK)
            return Response({"rating": None}, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response({"error": "Фильм не найден."}, status=status.HTTP_404_NOT_FOUND)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления активностями пользователей (Activity).
    """

    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
