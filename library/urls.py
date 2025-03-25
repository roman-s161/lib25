from django.urls import path, include
from . import views

app_name = 'library'

book_patterns = [
    path('book_list/', views.book_list, name='book_list'),
    path('add_book/', views.add_book, name='add_book'),
    path('book_detail/<int:book_id>/', views.book_detail, name='book_detail'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('confirm_delete_book/<int:book_id>/', views.confirm_delete_book, name='confirm_delete_book'),
]


reader_patterns = [
    path('reader_list/', views.reader_list, name='reader_list'),
    path('add_reader/', views.add_reader, name='add_reader'),
    path('reader_detail/<int:reader_id>/', views.reader_detail, name='reader_detail'),
    path('<int:reader_id>/edit/', views.edit_reader, name='edit_reader'),
    path('delete_reader/', views.delete_reader, name='delete_reader'),
    path('confirm_delete_reader/<int:reader_id>/', views.confirm_delete_reader, name='confirm_delete_reader'),
    path('edit_reader_form/', views.edit_reader_form, name='edit_reader_form'),
]


profile_patterns = [
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('borrowed_books/', views.user_borrowed_books, name='borrowed_books'),
    path('reading_history/', views.user_reading_history, name='reading_history'),
    path('edit_profile/', views.edit_user_profile, name='edit_profile'),
    path('return_book/<int:lending_id>/', views.return_book, name='return_book'),
]

urlpatterns = [
    
    path('book/', include((book_patterns, 'book'))),
    path('reader/', include((reader_patterns, 'reader'))),
    path('profile/', include((profile_patterns, 'profile'))),




    
    path('search/', views.search_books, name='search_books'),
    path('select_book_reader/', views.select_book_reader, name='select_book_reader'),
    path('', views.index, name='index'),
    path('books/<int:book_id>/borrow/', views.borrow_book, name='borrow_book'),
    path('lendings/overdue/', views.overdue_lendings, name='overdue_lendings'),
]