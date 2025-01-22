from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet, MovieViewSet, FriendViewSet, ListViewSet,
    ListMovieViewSet, RatingViewSet, ActivityViewSet, FriendsListView, FriendDetailView, ToggleFriendshipView,
    ProfileView, TopMoviesView, MovieSearchView, UserSearchView, UserListMoviesView, PublicFavoritesView, RateMovieView,
    MovieRatingView, FriendsActivityView
)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('friends', FriendViewSet)
router.register('lists', ListViewSet)
router.register('list-movies', ListMovieViewSet)
router.register('ratings', RatingViewSet)
router.register('activities', ActivityViewSet)
router.register("movies", MovieViewSet, basename="movie")

urlpatterns = [
    path('', include(router.urls)),

    path('friends-activity/', FriendsActivityView.as_view(), name='friends-activity'),
    path('friends/<int:user_id>/list/', FriendsListView.as_view(), name='friends-list'),
    path("friends/<int:friend_id>/details/", FriendDetailView.as_view(), name="friend-detail"),
    path("friends/<int:friend_id>/toggle/", ToggleFriendshipView.as_view(), name="toggle-friendship"),
    path("friends/<int:user_id>/favorites/", PublicFavoritesView.as_view(), name="friend-favorites"),

    path("profile/", ProfileView.as_view(), name="profile"),

    path('rate-movie/', RateMovieView.as_view(), name='rate-movie'),
    path('movies/<str:movie_id>/rating/', MovieRatingView.as_view(), name='movie-rating'),
    path('top-movies/', TopMoviesView.as_view(), name='top-movies'),

    path("api/movies/search/", MovieSearchView.as_view(), name="movie-search"),
    path("api/users/search/", UserSearchView.as_view(), name="user-search"),

    path('lists/<int:list_id>/movies/', UserListMoviesView.as_view(), name='user-list-movies'),
]
