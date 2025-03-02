from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid

class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    author = models.CharField(max_length=100, verbose_name='Автор')
    publication_date = models.DateField(verbose_name='Дата публикации')

    def __str__(self):
        return self.title
    
    def is_available(self):
        return not self.booklending_set.filter(status='reading').exists()
    
    def get_current_reader(self):
        lending = self.booklending_set.filter(status='reading').first()
        return lending.user if lending else None
    
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

