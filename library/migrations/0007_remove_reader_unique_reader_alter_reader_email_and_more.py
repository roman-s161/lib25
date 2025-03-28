# Generated by Django 5.1.6 on 2025-02-27 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_alter_book_options_alter_reader_options_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='reader',
            name='unique_reader',
        ),
        migrations.AlterField(
            model_name='reader',
            name='email',
            field=models.EmailField(default=None, max_length=254, unique=True, verbose_name='электронная\nпочта'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='name',
            field=models.CharField(max_length=50, verbose_name='ФИО читателя'),
        ),
    ]
