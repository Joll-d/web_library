# Generated by Django 4.1.7 on 2023-07-22 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryJ', '0008_website_book_description_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='book_author_path',
            field=models.CharField(default='', max_length=200),
        ),
    ]
