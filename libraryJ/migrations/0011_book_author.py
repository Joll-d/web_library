# Generated by Django 4.1.7 on 2023-07-23 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryJ', '0010_website_book_tags_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.CharField(default='', max_length=200),
        ),
    ]
