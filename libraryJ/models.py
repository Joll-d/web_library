from django.db import models

class Website(models.Model):
    name = models.CharField(max_length=200, unique=True)
    website_link = models.CharField(max_length=200, unique=True)
    image_link = models.CharField(max_length=200, default='')
    book_title_page_link_supplement = models.CharField(max_length=200, default='')

    book_title_path = models.CharField(max_length=200)
    chapter_title_path = models.CharField(max_length=200)

    book_description_path = models.CharField(max_length=200, default='')

    content_path = models.CharField(max_length=200)

    next_book_page_link_path = models.CharField(max_length=200)
    previous_book_page_link_path = models.CharField(max_length=200)

    book_title_page_length = models.IntegerField()

    art_path = models.CharField(max_length=200)

    create_time = models.DateTimeField(auto_now_add=True)


class Book(models.Model):
    Website = models.ForeignKey(Website, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=200)
    book_link = models.CharField(max_length=200)
    last_page_link = models.CharField(max_length=200)
    art_link = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    last_call_time = models.DateTimeField(auto_now_add=True)