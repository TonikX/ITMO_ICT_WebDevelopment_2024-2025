from django.urls import path
from .views import (
    ReadingRoomAPIView, BookListCreateAPIView, BookDetailAPIView, ReaderAPIView,
    BookTransactionListCreateAPIView, BookTransactionDetailAPIView, ReaderBooksAPIView, LateBooksAPIView,
    RemoveOldReadersAPIView, LibraryReportAPIView, ComplexLibraryReportAPIView,
    TransferBookAPIView, ManageBookCopiesAPIView, TransferReaderAPIView, ReadingRoomReadersAPIView,
    UpdateBookCodeAPIView, UpdateReaderTicketAPIView, LowStockBooksAPIView, ReadingRoomListAPIView
)

urlpatterns = [
    path('reading_rooms/', ReadingRoomAPIView.as_view(), name="reading_room_list_create"),
    path('books/', BookListCreateAPIView.as_view(), name="book_list_create"),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name="book_detail"),
    path('books/<int:pk>/discard/', BookDetailAPIView.as_view(), name="discard_book"),
    path('readers/', ReaderAPIView.as_view(), name="reader_list_create"),
    path('readers/<int:pk>/', ReaderAPIView.as_view(), name="reader_detail"),
    path('rooms/', ReadingRoomListAPIView.as_view(), name="rooms_list"),
    path('readers/<int:pk>/assign_room/', ReaderAPIView.as_view(), name="assign_reader_room"),
    path('book_transactions/', BookTransactionListCreateAPIView.as_view(), name="book_transaction_list_create"),
    path('book_transactions/<int:pk>/', BookTransactionDetailAPIView.as_view(), name="book_transaction_detail"),
    path('book_transactions/<int:pk>/return/', BookTransactionDetailAPIView.as_view(), name="mark_book_as_returned"),
    path('readers/<int:reader_id>/books/', ReaderBooksAPIView.as_view(), name="reader_books"),
    path('books/late/', LateBooksAPIView.as_view(), name="late_books"),
    path('readers/remove_old/', RemoveOldReadersAPIView.as_view(), name="remove_old_readers"),
    path('reports/', LibraryReportAPIView.as_view(), name="library_report"),
    path('reports/complex/', ComplexLibraryReportAPIView.as_view(), name="complex_library_report"),
    path('books/<int:book_id>/manage_copies/', ManageBookCopiesAPIView.as_view(), name="manage_book_copies"),
    path('books/<int:book_id>/transfer/', TransferBookAPIView.as_view(), name="transfer_book"),
    path('readers/<int:reader_id>/transfer/', TransferReaderAPIView.as_view(), name="transfer_reader"),
    path('reading_rooms/<int:room_id>/readers/', ReadingRoomReadersAPIView.as_view(), name="room_readers"),
    path('books/<int:book_id>/update_code/', UpdateBookCodeAPIView.as_view(), name="update_book_code"),
    path('readers/<int:reader_id>/update_ticket/', UpdateReaderTicketAPIView.as_view(), name="update_reader_ticket"),
    path('books/low_stock/', LowStockBooksAPIView.as_view(), name="low_stock_books"),
    path('reading_rooms/<int:pk>/', ReadingRoomAPIView.as_view(), name="reading_room_detail"),

]
