from django.views import generic
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from libraryJ.utils.utils import *
from libraryJ.utils.database_handler import *
from libraryJ.utils.parser import *
from libraryJ.utils.translator import *


class IndexView(generic.ListView):
    template_name = 'libraryJ/index.html'
    context_object_name = 'books'

    def get_queryset(self):

        return Book.objects.all()


class AddBookView(generic.ListView):
    template_name = 'libraryJ/add_book.html'
    context_object_name = 'add_book'

    def get_queryset(self):
        pass

    def post(self, request, *args, **kwargs):
        book_link = request.POST.get('bookLink')
        website_domain = get_domain_from_link(book_link)

        website = find_website_by_domain(website_domain)

        if website is None:
            return redirect("/add-website")
        else:
            book_title_link = get_book_title_link(book_link, website.book_title_page_length) + website.book_title_page_link_supplement

            parser = BookParser(book_title_link)
            book_title = parser.get_element_text(website.book_title_path)
            art_link = parser.get_element_src(website.art_path)
            book = Book.objects.create(
                Website = website,
                book_title = book_title,
                book_link = book_link,
                last_page_link = book_link,
                art_link = art_link,
            )
            return redirect("../")


class BookDeleteView(generic.DetailView):
    model = Book
    template_name = '/'
    success_url = '../'



class BookPageView(generic.DetailView):
    model = Book
    template_name = 'libraryJ/book_page.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        chapter_link = book.last_page_link
        website = book.Website
        
        parser = BookParser(chapter_link)
        chapter_title = parser.get_element_text(website.chapter_title_path)
        chapter_content = parser.get_elements_text(website.content_path)
    
        previous_chapter = parser.get_element_href(website.previous_book_page_link_path)
        next_chapter = parser.get_element_href(website.next_book_page_link_path)

        translator_en = Translator('en')
        chapter_title_en = translator_en.translate(chapter_title)
        chapter_content_en = translator_en.translate(chapter_content)

        translator_ru = Translator('ru')

        chapter_content_ru = translator_ru.translate(chapter_content)

        context['chapter_title'] = chapter_title_en
        context['chapter_content'] = zip(chapter_content_en, chapter_content_ru)

        context['previous_chapter'] = previous_chapter
        context['next_chapter'] = next_chapter
        return context
    
    def post(self, request, *args, **kwargs):
        book = self.get_object()
        
        book_link = request.POST.get("next_chapter")

        if book_link != 'None':
            book.last_page_link = book_link
            book.save()

        return redirect(f"/{book.pk}/")


class WebsiteView(generic.ListView):
    model = Website
    template_name = 'libraryJ/add_website.html'
    context_object_name = 'websites'

    def get_queryset(self):
        return Website.objects.all()

    def post(self, request, *args, **kwargs):
        website_link = request.POST.get('websiteLink')
        book_title_page_link = request.POST.get('bookTitlePageLink')
        book_chapter_page_link = request.POST.get('bookChapterPageLink')

        book_title_path = request.POST.get('bookTitle')
        art_path = request.POST.get('art')

        chapter_title_path = request.POST.get('chapterTitle')
        content_path = request.POST.get('content')

        next_book_page_link_path = request.POST.get('nextBookPageLink')
        previous_book_page_link_path = request.POST.get('previousBookPageLink')

        parser = BookParser(website_link)

        if 200 != (status_code:=(parser.get_website_status_code())):
            return HttpResponseBadRequest("Your error message here: " + str(status_code))
        
        website_domain = get_domain_from_link(website_link)

        website = find_website_by_domain(website_domain)
        website_name = get_website_name_from_link(website_link)

        image_link = parser.get_website_icon_src()

        book_title_page_link_supplement = get_book_title_page_link_supplement(book_title_page_link, book_chapter_page_link)

        book_title_page_length = get_book_title_page_length(book_title_page_link)
        
        website_data = {
            'name': website_name,
            'website_link': website_link,
            'book_title_page_link_supplement': book_title_page_link_supplement,
            'image_link': image_link,
            'book_title_path': book_title_path,
            'chapter_title_path': chapter_title_path,
            'content_path': content_path,
            'next_book_page_link_path': next_book_page_link_path,
            'previous_book_page_link_path': previous_book_page_link_path,
            'book_title_page_length': book_title_page_length,
            'art_path': art_path,
        }

        if website is None:
            website = Website.objects.create(**website_data)
        else:

            for key, value in website_data.items():
                setattr(website, key, value)
            website.save()

        return redirect("../")
    