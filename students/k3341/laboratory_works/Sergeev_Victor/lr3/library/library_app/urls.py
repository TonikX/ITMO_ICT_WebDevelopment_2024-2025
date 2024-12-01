from django.urls import path
from .views import *

urlpatterns = [
    path('genre/<int:pk>/', GenreRUDView.as_view()),
    path('genre/create', GenreCreateView.as_view()),
    path('genre/', GenreListView.as_view()),

    path('author/<int:pk>/', AuthorRUDView.as_view()),
    path('author/create/', AuthorCreateView.as_view()),
    path('author/', AuthorListView.as_view()),

    path('book/<int:pk>/', BookRUDView.as_view()),
    path('book/create/', BookCreateView.as_view()),
    path('book/', BookListView.as_view()),

    path('book_copy/', BookCopyListView.as_view()),
    path('book_copy/create/', BookCopyCreateView.as_view()),
    path('book_copy/<int:pk>/', BookCopyRUDView.as_view()),

    path('reader/<int:pk>/', ReaderRUDView.as_view()),
    path('reader/create/', ReaderCreateView.as_view()),
    path('reader/', ReaderListView.as_view()),

    path('room/<int:pk>/', ReadingRoomRUDView.as_view()),
    path('room/create/', ReadingRoomCreateView.as_view()),
    path('room/', ReadingRoomListView.as_view()),

    path('book_take/<int:pk>/', BookTakeRUDView.as_view()),
    path('book_take/create/', BookTakeCreateView.as_view()),

    path('reader/<int:pk>/book/', ReaderBooksView.as_view()),
    path('reader/delay/month/', ReadersMonthDelayView.as_view()),
    path('reader/less/5/', ReadersLessThanBooksView.as_view()),
    path('reader/age/young/', ReadersLessTwentyYears.as_view()),
    path('reader/education/stat/', ReadersEducationPercentageView.as_view()),
]