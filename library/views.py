from .forms import BookForm, ReaderForm
from .models import Book
from .models import Reader
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookIdForm, ReaderIdForm, SelectBookReaderForm


def select_book_reader(request):
    if request.method == 'POST':
        form = SelectBookReaderForm(request.POST)
        if form.is_valid():
            selection = form.cleaned_data['selection']
            book_id = form.cleaned_data['id']
            if selection == 'book':
                try:
                    book = Book.objects.get(id=book_id)
                    return redirect('book_detail', book_id=book_id)
                except Book.DoesNotExist:
                    return render(request, 'object_id_not_found.html' )
            elif selection == 'reader':
                try:
                    reader = Reader.objects.get(id=book_id)
                    return redirect('reader_detail', reader_id=book_id)
                except Reader.DoesNotExist:
                    return render(request, 'object_id_not_found.html' )
    else:
        form = SelectBookReaderForm()
    return render(request, 'select_book_reader.html', {'form': form})

def edit_book_form(request):
    if request.method == 'POST':
        form = BookIdForm(request.POST)
        if form.is_valid():
            book_id = form.cleaned_data['book_id']
            if not Book.objects.filter(id=book_id).exists():
                return render(request, 'object_id_not_found.html')
            return redirect('edit_book', book_id=book_id)
    else:
        form = BookIdForm()
    return render(request, 'edit_book_form.html', {'form': form})

def edit_reader_form(request):
    if request.method == 'POST':
        form = ReaderIdForm(request.POST)
        if form.is_valid():
            reader_id = form.cleaned_data['reader_id']
            if not Reader.objects.filter(id=reader_id).exists():
                return render(request, 'object_id_not_found.html')
            return redirect('edit_reader', reader_id=reader_id)
    else:
        form = ReaderIdForm()
    return render(request, 'edit_reader_form.html', {'form': form})

def index(request):
    return render(request, 'index.html')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Администраторы').exists())
def delete_book(request):
    if request.method == 'POST':
        book_id = request.POST['book_id']
        if not Book.objects.filter(id=book_id).exists():
            return render(request, 'object_id_not_found.html')
        return redirect('confirm_delete_book', book_id=book_id)
    return render(request, 'delete_book.html')

def confirm_delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'confirm_delete_book.html', {'book': book, 'book_id': book_id})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Администраторы').exists())
def delete_reader(request):
    if request.method == 'POST':
        reader_id = request.POST['reader_id']
        if not Reader.objects.filter(id=reader_id).exists():
            return render(request, 'object_id_not_found.html')
        return redirect('confirm_delete_reader', reader_id=reader_id)
    return render(request, 'delete_reader.html')

def confirm_delete_reader(request, reader_id):
    reader = get_object_or_404(Reader, id=reader_id)
    if request.method == 'POST':
        reader.delete()
        return redirect('reader_list')  # Перенаправление на страницу со списком читателей
    return render(request, 'confirm_delete_reader.html', {'reader': reader, 'reader_id': reader_id})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Администраторы').exists())
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')

            # Проверяем, существует ли книга с таким названием и автором
            if Book.objects.filter(title=title, author=author).exists():
                return render(request,'the object already exists.html')
            book = form.save()  # Сохраняем объект книги в переменную book
            book_id = book.id  # Получаем ID сохраненной книги
            return redirect('book_list')  # Перенаправляем на страницу со списком книг
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Администраторы').exists())
def add_reader(request):
    if request.method == 'POST':
        form = ReaderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            if Reader.objects.filter(name=name, email=email).exists():
                return render(request,'the object already exists.html')
            reader = form.save()
            return redirect('reader_list')
    else:
        form = ReaderForm()
    return render(request, 'add_reader.html', {'form': form})

def reader_list(request):
    readers = Reader.objects.all()
    return render(request, 'reader_list.html', {'readers': readers})



def book_list(request):
    books = Book.objects.all()  # Получаем все объекты книг из базы данных
    return render(request, 'book_list.html', {'books': books})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Администраторы').exists())
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', book_id=book_id)
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Администраторы').exists())
def edit_reader(request, reader_id):
    reader = get_object_or_404(Reader, id=reader_id)
    if request.method == 'POST':
        form = ReaderForm(request.POST, instance=reader)
        if form.is_valid():
            form.save()
            return redirect('reader_detail', reader_id=reader_id)
    else:
        form = ReaderForm(instance=reader)
    return render(request, 'edit_reader.html', {'form': form})




@login_required
@user_passes_test(lambda u: u.groups.filter(name='Библиотекари').exists())
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    author = book.author
    publication_date = book.publication_date
    return render(request, 'book_detail.html', {'book': book, 'author': author, 'publication_date': publication_date})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Библиотекари').exists())
def reader_detail(request, reader_id):
    reader = get_object_or_404(Reader, id=reader_id)
    books = reader.books_read.all()
    return render(request, 'reader_detail.html', {'reader': reader, 'books': books})



