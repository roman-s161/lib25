from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    author = models.CharField(max_length=100, verbose_name='Автор')
    publication_date = models.DateField(verbose_name='Дата публикации')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Reader(models.Model):
    name = models.CharField(max_length=100, verbose_name='ФИО читателя')
    email = models.EmailField(verbose_name='электронная\nпочта', default=None)
    books_read = models.ManyToManyField(Book, verbose_name='прочитанные книги')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'





