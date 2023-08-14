from ..models import Website
from ..models import Book
from ..models import Chapter
from django.utils import timezone
from libraryJ.utils.parser import *
from libraryJ.utils.translator import *


def find_website_by_domain(website_domain):
    try:
        name = website_domain.split('.')
        website = Website.objects.get(name=name[1])
        return website
    except Website.DoesNotExist:
        return None


def create_chapters(book: Book):
    website = book.Website

    chapter_number = 1
    chapter_link = book.first_chapter_link
    print(chapter_link)
    
    while chapter_link is not None:
        parser = BookParser(chapter_link)
        chapter_title = parser.get_element_text(website.chapter_title_path)
        chapter_content = parser.get_elements_text(website.book_content_path)
        next_chapter = parser.get_element_href(
                website.next_chapter_link_path)

        translator_en = Translator('en')
        chapter_title_en = translator_en.translate(chapter_title)
        chapter_content_en = translator_en.translate(chapter_content)

        translator_ru = Translator('ru')
        chapter_content_ru = translator_ru.translate(chapter_content)

        chapter = Chapter.objects.create(
        book = book,
        title = chapter_title_en,
        content_en = chapter_content_en,
        content_ru = chapter_content_ru,

        chapter_number = chapter_number,
        release_date = timezone.now(),
        )
        
        print(chapter.title)
        chapter_number += 1
        chapter_link = next_chapter



def get_first_chapter_link(website: Website, chapter_link: str):
    previous_chapter_link_path = chapter_link

    while True:
        parser = BookParser(previous_chapter_link_path)

        previous_chapter_link_path = parser.get_element_href(
                website.previous_chapter_link_path)
        
        if previous_chapter_link_path is None:
            break

        first_chapter_link = previous_chapter_link_path

    return first_chapter_link