# Generated by Django 4.1.7 on 2023-08-14 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryJ', '0014_book_is_update_chapter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='last_chapter_link',
        ),
        migrations.AddField(
            model_name='book',
            name='last_chapter',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
