from .forms import BookForm, ReaderForm
from django.db.models import Q
from .models import Book, Reader, BookLending
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookIdForm, ReaderIdForm, SelectBookReaderForm
from django.contrib import messages
from django.utils import timezone




def index(request):
    recommended_books = Book.objects.filter(rating__gte=4.0).order_by('-rating')[:8]
    return render(request, 'index.html', {'recommended_books': recommended_books})

@login_required
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
        form = BookForm(request.POST, request.FILES)
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
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Книга успешно удалена')
        return redirect('library:book:book_list')
    return render(request, 'library/confirm_delete_book.html', {'book': book})


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



def search_books(request):
    query = request.GET.get('query', '').strip()
    books = []
    
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genre__icontains=query)
        ).distinct()
        
    return render(request, 'library/search_results.html', {
        'books': books,
        'query': query,
        'total_results': len(books)
    })


@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        try:
            BookLending.borrow_book(request.user, book)
            messages.success(request, 'Вы успешно взяли книгу')
        except Exception as e:
            messages.error(request, str(e))
        return redirect('library:book:book_detail', book_id=book.id)
    return render(request, 'library/borrow_book.html', {'book': book})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name__in=['Администраторы', 'Библиотекари']).exists())
def overdue_lendings(request):
    lendings = BookLending.get_overdue_lendings()
    now = timezone.now().date()
    return render(request, 'library/overdue_lendings.html', {'lendings': lendings, 'now': now})

# Личный кабинет пользователя - главная страница
@login_required
def user_dashboard(request):
    # Получаем текущие выдачи книг пользователя
    active_lendings = BookLending.objects.filter(
        user=request.user,
        status='reading'
    ).order_by('return_due_date')
    
    # Получаем количество просроченных книг
    overdue_count = active_lendings.filter(
        return_due_date__lt=timezone.now().date()
    ).count()
    
    # Получаем общее количество прочитанных книг
    read_books_count = BookLending.objects.filter(
        user=request.user,
        status='returned'
    ).count()
    
    # Получаем рекомендованные книги (например, по жанрам, которые читал пользователь)
    # Это простая реализация - можно улучшить алгоритм рекомендаций
    favorite_genres = BookLending.objects.filter(
        user=request.user
    ).values_list('book__genre', flat=True).distinct()
    
    recommended_books = Book.objects.filter(
        genre__in=favorite_genres
    ).exclude(
        booklending__user=request.user
    ).order_by('-rating')[:5]
    
    context = {
        'active_lendings': active_lendings,
        'overdue_count': overdue_count,
        'read_books_count': read_books_count,
        'recommended_books': recommended_books,
    }
    
    return render(request, 'library/profile/dashboard.html', context)

# Список книг, которые пользователь сейчас читает
@login_required
def user_borrowed_books(request):
    active_lendings = BookLending.objects.filter(
        user=request.user,
        status='reading'
    ).order_by('return_due_date')
    
    return render(request, 'library/profile/borrowed_books.html', {
        'active_lendings': active_lendings
    })

# История чтения пользователя
@login_required
def user_reading_history(request):
    reading_history = BookLending.objects.filter(
        user=request.user,
        status='returned'
    ).order_by('-returned_date')
    
    return render(request, 'library/profile/reading_history.html', {
        'reading_history': reading_history
    })

@login_required
def edit_user_profile(request):
    if request.method == 'POST':
        # Обновляем только определенные поля
        user = request.user
        
        # Обновляем поле name
        user.name = request.POST.get('name', user.name)
        
        # Также обновляем first_name и last_name для отображения в админке
        name_parts = user.name.split()
        if len(name_parts) >= 1:
            user.first_name = name_parts[0]
            if len(name_parts) >= 2:
                user.last_name = ' '.join(name_parts[1:])
            else:
                user.last_name = ''
        
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.address = request.POST.get('address', user.address)
        
        # Обработка загрузки фото профиля
        if 'profile_photo' in request.FILES:
            user.profile_photo = request.FILES['profile_photo']
        
        user.save()
        messages.success(request, 'Профиль успешно обновлен')
        return redirect('library:profile:dashboard')
    
    return render(request, 'library/profile/edit_profile.html', {
        'user': request.user
    })

# Возврат книги пользователем (запрос на возврат)
@login_required
def return_book(request, lending_id):
    lending = get_object_or_404(BookLending, id=lending_id, user=request.user)
    
    if lending.status != 'reading':
        messages.error(request, 'Эта книга уже возвращена или не может быть возвращена')
        return redirect('library:profile:borrowed_books')
    
    if request.method == 'POST':
        # Отмечаем книгу как возвращенную
        lending.status = 'returned'
        lending.returned_date = timezone.now().date()
        lending.save()
        
        # Увеличиваем количество доступных копий
        lending.book.increase_available_copies()
        
        messages.success(request, f'Книга "{lending.book.title}" успешно возвращена')
        return redirect('library:profile:borrowed_books')
    
    return render(request, 'library/profile/return_book.html', {
        'lending': lending
    })

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name__in=['Администраторы', 'Библиотекари']).exists())
def confirm_return_book(request, lending_id):
    lending = get_object_or_404(BookLending, id=lending_id)
    now = timezone.now().date()
    
    return render(request, 'library/confirm_return_book.html', {
        'lending': lending,
        'now': now
    })

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name__in=['Администраторы', 'Библиотекари']).exists())
def librarian_return_book(request, lending_id):
    lending = get_object_or_404(BookLending, id=lending_id)
    
    if request.method == 'POST':
        lending.status = 'returned'
        lending.returned_date = timezone.now().date()
        lending.save()
        
        lending.book.increase_available_copies()
        
        messages.success(request, f'Книга "{lending.book.title}" успешно возвращена')
        return redirect('library:overdue_lendings')
    
    now = timezone.now().date()
    return render(request, 'library/confirm_return_book.html', {
        'lending': lending,
        'now': now
    })

