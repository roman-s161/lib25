from django.contrib import admin
from .models import Book, Reader
from django.contrib.auth.models import Group

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'publication_date', 'genre', 'rating')
    list_filter = ('genre', 'rating')
    search_fields = ('title', 'author', 'genre')
    list_editable = ('rating',)
    ordering = ('-publication_date',)
    list_per_page = 20

@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_full_name', 'get_groups', 'is_staff', 'email')
    list_display_links = ('get_full_name',)
    list_filter = ('groups', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    
    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    
    get_full_name.short_description = 'ФИО'
    get_groups.short_description = 'Группы'


