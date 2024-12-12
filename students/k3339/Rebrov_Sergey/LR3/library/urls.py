from django.urls import path
from .views import *

app_name = "library"

urlpatterns = [
   path('books/', BooksAPIView.as_view()),
   path('books/<int:pk>', BookAPIView.as_view()),
   path('authors/', AuthorsAPIView.as_view()),
   path('authors/<int:pk>', AuthorAPIView.as_view()),
   path('publishers/', PublishersAPIView.as_view()),
   path('publishers/<int:pk>', PublisherAPIView.as_view()),
   path('libraries/', LibrariesAPIView.as_view()),
   path('libraries/<int:pk>', LibraryAPIView.as_view()),
   path('halls/', HallsAPIView.as_view()),
   path('halls/<int:pk>', HallAPIView.as_view()),
   path('readers/', ReadersAPIView.as_view()),
   path('readers/<int:pk>', ReaderAPIView.as_view()),

   path('rent_book/', RentBookAPIView.as_view()),
   path('return_book/', ReturnBookAPIView.as_view()),
   path('add_book/', AddBookAPIView.as_view()),
   path('remove_book/', RemoveBookAPIView.as_view())
]
