from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Book, Reader
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass

@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    pass
