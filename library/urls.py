from django.urls import path
from . import views

app_name = 'library'


urlpatterns = [
    path('book_list', views.book_list, name='book_list'),
    path('add_book/', views.add_book, name='add_book'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('confirm_delete/<int:book_id>/', views.confirm_delete_book, name='confirm_delete_book'),


    path('reader_list', views.reader_list, name='reader_list'),
    path('add_reader/', views.add_reader, name='add_reader'),
    path('<int:reader_id>/', views.reader_detail, name='reader_detail'),
    path('<int:reader_id>/edit/', views.edit_reader, name='edit_reader'),
    path('delete/<int:reader_id>/', views.delete_reader, name='delete_reader'),
    path('confirm_delete/<int:reader_id>/', views.confirm_delete_reader, name='confirm_delete_reader'),


    path('select_book_reader/', views.select_book_reader, name='select_book_reader'),
    path('edit_book/', views.edit_book_form, name='edit_book_form'),
    path('edit_reader/', views.edit_reader_form, name='edit_reader_form'),
    path('', views.index, name='index'),
]
