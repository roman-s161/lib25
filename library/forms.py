from django import forms
from .models import Book, Reader

class ReaderForm(forms.ModelForm):
    name = forms.CharField(
        label='ФИО',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ФИО'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )
    phone = forms.CharField(
        label='Телефон',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите телефон'
        })
    )
    address = forms.CharField(
        label='Адрес',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Введите адрес'
        })
    )
    profile_photo = forms.ImageField(
        label='Фото',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )
    books_read = forms.ModelMultipleChoiceField(
        queryset=Book.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'list-unstyled'
        }),
        label='Прочитанные книги',
        to_field_name='title',
        required=False
    )

    class Meta:
        model = Reader
        fields = ['name', 'email', 'phone', 'address', 'profile_photo', 'books_read']

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        qs = Reader.objects.filter(email__iexact=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Читатель с такой электронной почтой уже существует.")
        return email


class BookForm(forms.ModelForm):
    title = forms.CharField(
        label='Название',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название книги'
        })
    )
    author = forms.CharField(
        label='Автор',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите автора'
        })
    )
    publication_date = forms.DateField(
        label='Дата публикации',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    description = forms.CharField(
        label='Описание книги',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Введите описание книги'
        })
    )
    genre = forms.CharField(
        label='Жанр',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите жанр'
        })
    )
    pages = forms.IntegerField(
        label='Количество страниц',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите количество страниц'
        })
    )
    publisher = forms.CharField(
        label='Издательство',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите издательство'
        })
    )
    language = forms.CharField(
        label='Язык издания',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите язык издания'
        })
    )
    total_copies = forms.IntegerField(
        label='Количество копий',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите количество копий'
        })
    )
    cover_image = forms.ImageField(
        label='Обложка книги',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date', 'description', 'genre', 
                 'pages', 'publisher', 'language', 'total_copies', 'cover_image']


class BookIdForm(forms.Form):
    book_id = forms.IntegerField(label='ID книги')

class ReaderIdForm(forms.Form):
    reader_id = forms.IntegerField(label='ID читателя')

class SelectBookReaderForm(forms.Form):
    CHOICES = [('book', 'Книгу'), ('reader', 'Читателя')]
    selection = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect,label='выбрать')
    id = forms.IntegerField(label='ID')
