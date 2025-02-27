from django import forms
from .models import Book, Reader

class ReaderForm(forms.ModelForm):
    books_read = forms.ModelMultipleChoiceField(
        queryset=Book.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Прочитанные книги',
        to_field_name='title', # Указываем поле 'title' для отображения названий книг
        required=False # Поле не обязательно для заполнения
    )

    class Meta:
        model = Reader
        fields = ['name', 'email', 'books_read']

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        qs = Reader.objects.filter(email__iexact=email)
        # Если редактирование существующей записи, исключаем её из проверки
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Читатель с такой электронной почтой уже существует.")
        return email


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date']

class BookIdForm(forms.Form):
    book_id = forms.IntegerField(label='ID книги')

class ReaderIdForm(forms.Form):
    reader_id = forms.IntegerField(label='ID читателя')

class SelectBookReaderForm(forms.Form):
    CHOICES = [('book', 'Книгу'), ('reader', 'Читателя')]
    selection = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect,label='выбрать')
    id = forms.IntegerField(label='ID')
