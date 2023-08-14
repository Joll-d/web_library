# Generated by Django 4.1.7 on 2023-08-14 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libraryJ', '0013_rename_art_link_book_first_chapter_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_update',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content_en', models.TextField()),
                ('content_ru', models.TextField()),
                ('chapter_number', models.PositiveIntegerField()),
                ('release_date', models.DateField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraryJ.book')),
            ],
            options={
                'ordering': ['chapter_number'],
            },
        ),
    ]
