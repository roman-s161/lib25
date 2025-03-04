from .forms import BookForm, ReaderForm
from .models import Book
from .models import Reader
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookIdForm, ReaderIdForm, SelectBookReaderForm
from django.contrib import messages


def index(request):
    return render(request, 'index.html')

def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

def reader_list(request):
    readers = Reader.objects.all()
    return render(request, 'library/reader_list.html', {'readers': readers})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name__in=['Администраторы', 'Библиотекари']).exists())
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')

            if Book.objects.filter(title=title, author=author).exists():
                messages.error(request, 'Такая книга уже существует')
                return render(request,'library/add_book.html', {'form': form})
            
            form.save()
            messages.success(request, 'Новая книга успешно добавлена', extra_tags='success')
            return redirect('library:book:book_list')
    else:
        form = BookForm()
    return render(request, 'library/add_book.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name__in=['Администраторы', 'Библиотекари']).exists())
def add_reader(request):
    if request.method == 'POST':
        form = ReaderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('library:reader:reader_list')
    else:
        form = ReaderForm()
    return render(request, 'library/add_reader.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name__in=['Администраторы', 'Библиотекари']).exists())
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Книга успешно отредактирована')
            return redirect('library:book:book_detail', book_id=book_id)
    else:
        form = BookForm(instance=book)
    return render(request, 'library/edit_book.html', {'form': form})

def edit_book_form(request):
    if request.method == 'POST':
        form = BookIdForm(request.POST)
        if form.is_valid():
            book_id = form.cleaned_data['book_id']
            if not Book.objects.filter(id=book_id).exists():
                return render(request, 'library/object_id_not_found.html')
            return redirect('library:book:edit_book', book_id=book_id)
    else:
        form = BookIdForm()
    return render(request, 'library/edit_book_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name__in=['Администраторы', 'Библиотекари']).exists())
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    author = book.author
    publication_date = book.publication_date
    return render(request, 'library/book_detail.html', {'book': book, 'author': author, 'publication_date': publication_date})

def select_book_reader(request):
    if request.method == 'POST':
        form = SelectBookReaderForm(request.POST)
        if form.is_valid():
            selection = form.cleaned_data['selection']
            book_id = form.cleaned_data['id']
            if selection == 'book':
                try:
                    book = Book.objects.get(id=book_id)
                    return redirect('library:book:book_detail', book_id=book_id)
                except Book.DoesNotExist:
                    return render(request, 'library/object_id_not_found.html' )
            elif selection == 'reader':
                try:
                    reader = Reader.objects.get(id=book_id)
                    return redirect('library:reader:reader_detail', reader_id=book_id)
                except Reader.DoesNotExist:
                    return render(request, 'library/object_id_not_found.html' )
    else:
        form = SelectBookReaderForm()
    return render(request, 'library/select_book_reader.html', {'form': form})

def edit_reader_form(request):
    if request.method == 'POST':
        form = ReaderIdForm(request.POST)
        if form.is_valid():
            reader_id = form.cleaned_data['reader_id']
            if not Reader.objects.filter(id=reader_id).exists():
                return render(request, 'library/object_id_not_found.html')
            return redirect('library:reader:edit_reader', reader_id=reader_id)
    else:
        form = ReaderIdForm()
    return render(request, 'library/edit_reader_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Администраторы').exists())
def delete_book(request):
    if request.method == 'POST':
        book_id = request.POST['book_id']
        if not Book.objects.filter(id=book_id).exists():
            return render(request, 'library/object_id_not_found.html')
        return redirect('library:book:confirm_delete_book', book_id=book_id)
    messages.warning(request, 'Книга удалена из библиотеки')
    return render(request, 'library/delete_book.html')

def confirm_delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('library:book:book_list')
    return render(request, 'library/confirm_delete_book.html', {'book': book, 'book_id': book_id})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Администраторы').exists())
def delete_reader(request):
    if request.method == 'POST':
        reader_id = request.POST['reader_id']
        if not Reader.objects.filter(id=reader_id).exists():
            return render(request, 'library/object_id_not_found.html')
        return redirect('library:reader:confirm_delete_reader', reader_id=reader_id)
    return render(request, 'library/delete_reader.html')

def confirm_delete_reader(request, reader_id):
    reader = get_object_or_404(Reader, id=reader_id)
    if request.method == 'POST':
        reader.delete()
        return redirect('library:reader:reader_list')  # Перенаправление на страницу со списком читателей
    return render(request, 'library/confirm_delete_reader.html', {'reader': reader, 'reader_id': reader_id})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name__in=['Администраторы', 'Библиотекари']).exists())
def edit_reader(request, reader_id):
    reader = get_object_or_404(Reader, id=reader_id)
    if request.method == 'POST':
        form = ReaderForm(request.POST, instance=reader)
        if form.is_valid():
            form.save()
            return redirect('library:reader:reader_detail', reader_id=reader_id)
    else:
        form = ReaderForm(instance=reader)
    return render(request, 'library/edit_reader.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name__in=['Администраторы', 'Библиотекари']).exists())
def reader_detail(request, reader_id):
    reader = get_object_or_404(Reader, id=reader_id)
    books = reader.books_read.all()
    return render(request, 'library/reader_detail.html', {'reader': reader, 'books': books})



