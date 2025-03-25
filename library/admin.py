from django.contrib import admin
from .models import Book, Reader, BookLending
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.utils import timezone

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

@admin.register(BookLending)
class BookLendingAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_name', 'get_book_title', 'borrowed_date', 
                    'return_due_date', 'returned_date', 'get_status_colored', 'get_days_remaining')
    list_filter = ('status', 'borrowed_date', 'return_due_date')
    search_fields = ('user__name', 'book__title')
    readonly_fields = ('borrowed_date',)
    list_per_page = 20
    date_hierarchy = 'borrowed_date'
    
    def get_user_name(self, obj):
        return obj.user.name
    get_user_name.short_description = 'Читатель'
    get_user_name.admin_order_field = 'user__name'
    
    def get_book_title(self, obj):
        return obj.book.title
    get_book_title.short_description = 'Книга'
    get_book_title.admin_order_field = 'book__title'
    
    def get_status_colored(self, obj):
        colors = {
            'reading': 'blue',
            'returned': 'green',
            'overdue': 'red'
        }
        status_display = dict(obj._meta.get_field('status').choices)[obj.status]
        return format_html('<span style="color: {};">{}</span>', colors[obj.status], status_display)
    get_status_colored.short_description = 'Статус'
    get_status_colored.admin_order_field = 'status'
    
    def get_days_remaining(self, obj):
        if obj.status == 'returned':
            return '-'
        
        today = timezone.now().date()
        if obj.return_due_date < today:
            days = (today - obj.return_due_date).days
            return format_html('<span style="color: red;">Просрочено на {} дн.</span>', days)
        else:
            days = (obj.return_due_date - today).days
            return format_html('<span style="color: green;">Осталось {} дн.</span>', days)
    get_days_remaining.short_description = 'Дней до/после возврата'
    
    actions = ['mark_as_returned', 'mark_as_overdue']
    
    def mark_as_returned(self, request, queryset):
        updated = queryset.update(status='returned', returned_date=timezone.now().date())
        self.message_user(request, f'Отмечено как возвращено: {updated} записей')
    mark_as_returned.short_description = 'Отметить как возвращенные'
    
    def mark_as_overdue(self, request, queryset):
        updated = queryset.update(status='overdue')
        self.message_user(request, f'Отмечено как просроченные: {updated} записей')
    mark_as_overdue.short_description = 'Отметить как просроченные'



