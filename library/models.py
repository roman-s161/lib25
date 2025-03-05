from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
import random

class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    author = models.CharField(max_length=100, verbose_name='Автор')
    publication_date = models.DateField(verbose_name='Дата публикации')
    description = models.TextField(verbose_name='Описание книги', blank=True, default='')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name='Рейтинг')
    isbn = models.CharField(max_length=13, verbose_name='ISBN', unique=True, blank=True, null=True)
    genre = models.CharField(max_length=50, verbose_name='Жанр', default='Не указан')
    pages = models.IntegerField(verbose_name='Количество страниц', default=0)
    publisher = models.CharField(max_length=100, verbose_name='Издательство', default='Не указано')
    cover_image = models.ImageField(upload_to='book_covers/', verbose_name='Обложка', blank=True, null=True)
    language = models.CharField(max_length=30, verbose_name='Язык издания', default='Русский')
    available_copies = models.IntegerField(default=1, verbose_name='Количество доступных копий')
    total_copies = models.IntegerField(default=1, verbose_name='Всего копий')


    def __str__(self):
        return self.title
    
    def is_available(self):
        return not self.booklending_set.filter(status='reading').exists()
    
    def get_current_reader(self):
        lending = self.booklending_set.filter(status='reading').first()
        return lending.user if lending else None
    
    def get_rating_display(self):
        return f"{self.rating}/5.00"
    
    def decrease_available_copies(self):
        if self.available_copies > 0:
            self.available_copies -= 1
            self.save()
            
    def increase_available_copies(self):
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            self.save()
    
    def save(self, *args, **kwargs):
        if not self.isbn:
            # Генерируем ISBN-13
            # 978 - префикс для книг
            # XXXX - код издательства (рандомно для примера)
            # XXXXX - номер издания
            # X - контрольная цифра
            isbn_prefix = '978'
            publisher_code = str(random.randint(1000, 9999))
            edition_number = str(random.randint(10000, 99999))
            isbn_without_check = f"{isbn_prefix}{publisher_code}{edition_number}"
            
            # Вычисляем контрольную цифру
            total = 0
            for i in range(12):
                if i % 2 == 0:
                    total += int(isbn_without_check[i])
                else:
                    total += int(isbn_without_check[i]) * 3
            check_digit = (10 - (total % 10)) % 10
            
            self.isbn = f"{isbn_without_check}{check_digit}"
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Reader(AbstractUser):
    ROLE_CHOICES = (
        ('reader', 'Читатель'),
        ('librarian', 'Библиотекарь'),
        ('admin', 'Администратор'),
    )
    name = models.CharField(max_length=50, verbose_name='ФИО читателя')
    username = models.CharField('Username', max_length=150, unique=True, default='user')
    email = models.EmailField(verbose_name='электронная\nпочта', default=None, unique=True)
    books_read = models.ManyToManyField(Book, verbose_name='прочитанные книги', blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader')
    profile_photo = models.ImageField('Фото профиля', upload_to='profile_photos/', null=True, blank=True)
    address = models.TextField('Адрес проживания', blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    library_card_number = models.CharField('Номер читательского билета', max_length=50, unique=True, default='LIB-{}'.format(uuid.uuid4().hex[:8].upper()))
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='reader_set',
        related_query_name='reader'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='reader_set',
        related_query_name='reader'
    )
    password = models.CharField('Password', max_length=128, default='defaultpassword')

    def __str__(self):
        return self.name
    
    def get_active_lendings(self):
        return self.book_lendings.filter(status='reading')
    
    def get_overdue_books(self):
        return self.book_lendings.filter(status='overdue')
    
    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'
        permissions = [
            ("can_lend_books", "Can lend books to readers"),
            ("can_view_all_readers", "Can view all readers")
        ]

class BookLending(models.Model):
    user = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='book_lendings')
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    borrowed_date = models.DateField('Дата выдачи')
    return_due_date = models.DateField('Дата возврата')
    returned_date = models.DateField('Фактическая дата возврата', null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('reading', 'Читает'),
        ('returned', 'Возвращена'),
        ('overdue', 'Просрочена')
    ])

    def update_status(self):
        today = timezone.now().date()
        if self.returned_date:
            self.status = 'returned'
        elif today > self.return_due_date:
            self.status = 'overdue'
        else:
            self.status = 'reading'
        self.save()

