from django.db import models
from django.contrib.postgres.fields import ArrayField


class Website(models.Model):
    name = models.CharField(max_length=200, unique=True)
    website_link = models.CharField(max_length=200, unique=True)
    icon_link = models.CharField(max_length=200, default='')
    book_title_page_link_supplement = models.CharField(
        max_length=200, default='')

    book_author_path = models.CharField(max_length=200, default='')
    book_tags_path = models.CharField(max_length=200, default='')

    book_title_path = models.CharField(max_length=200)
    chapter_title_path = models.CharField(max_length=200)

    book_description_path = models.CharField(max_length=200, default='')

    book_content_path = models.CharField(max_length=200)

    next_chapter_link_path = models.CharField(max_length=200)
    previous_chapter_link_path = models.CharField(max_length=200)

    book_title_page_length = models.IntegerField()

    book_image_path = models.CharField(max_length=200)

    create_time = models.DateTimeField(auto_now_add=True)


class Book(models.Model):
    Website = models.ForeignKey(Website, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, default='')
    tags = ArrayField(models.CharField(max_length=50),
                      blank=True, default=list)
    description = ArrayField(models.CharField(
        max_length=5000), blank=True, default=list)

    first_chapter_link = models.CharField(max_length=200)
    last_chapter = models.PositiveIntegerField(default=1)
    image_link = models.CharField(max_length=200)

    is_update = models.BooleanField(default=False)

    create_time = models.DateTimeField(auto_now_add=True)
    last_call_time = models.DateTimeField(auto_now_add=True)


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content_en = ArrayField(models.CharField(max_length=5000),
                      blank=True, default=list)
    content_ru = ArrayField(models.CharField(max_length=5000),
                      blank=True, default=list)

    chapter_number = models.PositiveIntegerField()
    release_date = models.DateField()

    class Meta:
        ordering = ['chapter_number']
