from django.forms.models import BaseModelForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect


from libraryJ.utils.utils import *
from libraryJ.utils.database_handler import *
from libraryJ.utils.parser import *
from libraryJ.utils.translator import *
from django.contrib import messages
from django.utils import timezone
from .forms import *
import threading

class IndexView(generic.ListView):
    template_name = 'libraryJ/index.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.all().order_by('-last_call_time')


class BookIndexView(generic.DetailView):
    model = Book
    template_name = 'libraryJ/index_book.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()

        description_en = book.description
        author = book.author
        tags = book.tags

        context['description_en'] = description_en
        context['author'] = author
        context['tags'] = tags

        return context


class BookCreateView(generic.CreateView):
    model = Book
    template_name = 'libraryJ/create_book.html'
    form_class = BookCreateForm

    def post(self, request, *args, **kwargs):
        first_chapter_link = request.POST.get('first_chapter_link')
        website_domain = get_domain_from_link(first_chapter_link)

        website = find_website_by_domain(website_domain)

        if website is None:
            return redirect(reverse_lazy("library:create-website"))
        else:
            book_title_link = get_book_title_link(
                first_chapter_link, website.book_title_page_length) + website.book_title_page_link_supplement

            parser = BookParser(book_title_link)
            title = parser.get_element_text(website.book_title_path)
            image_link = parser.get_element_src(website.book_image_path)

            author = 'None'
            if website.book_author_path != '':
                author = parser.get_element_text(website.book_author_path)

            tags = ['None']
            if website.book_tags_path != '':
                tags = parser.get_elements_text(website.book_tags_path)

            description = ['None']
            if website.book_description_path != '':
                description = parser.get_elements_text(
                    website.book_description_path)

            first_chapter_link = get_first_chapter_link(website, first_chapter_link)

            book = Book.objects.create(
                Website=website,
                title=title,
                first_chapter_link=first_chapter_link,
                image_link=image_link,

                author=author,
                tags=tags,
                description=description,
            )

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(create_chapters(book))
            loop.close()

            return redirect(reverse_lazy('library:index-library'))


class BookUpdateView(generic.DetailView):
    model = Book
    template_name = "libraryJ/index_book.html"

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        website = book.Website

        book_title_link = get_book_title_link(
            book.first_chapter_link, website.book_title_page_length) + website.book_title_page_link_supplement

        parser = BookParser(book_title_link)

        PARSING_TYPE_STRING = 'str'
        PARSING_TYPE_LIST_OF_STRINGS = 'list(str)'
        PARSING_TYPE_SOURCE = 'src'

        attributes_mapping = {
            website.book_title_path: ('title', PARSING_TYPE_STRING),
            website.book_image_path: ('image_link', PARSING_TYPE_SOURCE),
            website.book_author_path: ('author', PARSING_TYPE_STRING),
            website.book_tags_path: ('tags', PARSING_TYPE_LIST_OF_STRINGS),
            website.book_description_path: (
                'description', PARSING_TYPE_LIST_OF_STRINGS)
        }

        for path, (attribute, parsing_type) in attributes_mapping.items():
            if parsing_type == 'str':
                element_value = parser.get_element_text(path)
                setattr(book, attribute,
                        element_value if element_value else 'None')
            elif parsing_type == 'list(str)':
                element_values = parser.get_elements_text(path)
                setattr(book, attribute,
                        element_values if element_values else ['None'])
            elif parsing_type == 'src':
                setattr(book, attribute, parser.get_element_src(
                    path) if path else 'None')

        book.save()

        return redirect(reverse_lazy('library:index-book', kwargs={'pk': self.kwargs['pk']}))


class BookDeleteView(generic.DetailView):
    model = Book
    success_url = reverse_lazy('library:index-library')

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        confirmation = request.POST.get('deleteConfirmation')
        if confirmation == 'I am sure':
            book.delete()

        return redirect(reverse_lazy('library:index-library'))
    

class BookPageView(generic.DetailView):
    model = Book
    template_name = 'libraryJ/book_page.html'
    context_object_name = 'book'

    def get(self, request, chapter_pk, *args, **kwargs):
        self.chapter_pk = chapter_pk
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chapter_pk = self.chapter_pk
        book = self.get_object()
        chapter = Chapter.objects.filter(book=book, chapter_number=chapter_pk).first()
        previous_chapter = Chapter.objects.filter(book=book, chapter_number=chapter_pk-1).first()
        next_chapter = Chapter.objects.filter(book=book, chapter_number=chapter_pk+1).first()

        chapter_title_en = chapter.title

        chapter_content_en = chapter.content_en
        chapter_content_ru = chapter.content_ru
        context['chapter_title'] = chapter_title_en
        context['chapter_content'] = zip(
            chapter_content_en, chapter_content_ru)
        
        context['previous_chapter'] = previous_chapter.chapter_number if previous_chapter else 0
        context['next_chapter'] = next_chapter.chapter_number if next_chapter else 0

        book.last_call_time = timezone.now()
        book.save()

        return context

    def post(self, request, *args, **kwargs):
        book = self.get_object()

        book_link = request.POST.get("chapter_link")

        if book_link != 0:
            book.last_chapter_link = book_link
            book.save()

        return redirect(reverse_lazy('library:book-page', kwargs={'pk': book.pk, 'chapter_pk': book_link}))


class WebsiteView(generic.ListView):
    model = Website
    template_name = 'libraryJ/index_website.html'
    context_object_name = 'websites'

    def get_queryset(self):
        return Website.objects.all()
    

class WebsiteCreateView(generic.CreateView):
    model = Website
    form_class = WebsiteCreateForm
    template_name = 'libraryJ/create_website.html'
    success_url = reverse_lazy('library:index-library')

    def form_valid(self, form):
            book_title_page_link = form.cleaned_data['book_title_page_link']
            book_chapter_page_link = form.cleaned_data['book_chapter_page_link']

            website = form.save(commit=False)
            website_link = website.website_link

            parser = BookParser(website_link)
            name = get_website_name_from_link(website_link)
            icon_link = parser.get_website_icon_src()
            book_title_page_link_supplement = get_book_title_page_link_supplement(
                book_title_page_link, book_chapter_page_link)
            book_title_page_length = get_book_title_page_length(
                book_title_page_link)

            website.name = name
            website.icon_link = icon_link
            website.book_title_page_link_supplement = book_title_page_link_supplement
            website.book_title_page_length = book_title_page_length

            website.save()

            return redirect(reverse_lazy('library:index-website'))


class WebsiteUpdateView(generic.UpdateView):
    model = Website
    form_class = WebsiteUpdateForm
    template_name = 'libraryJ/update_website.html'
    context_object_name = 'website'
    success_url = reverse_lazy('library:index-library')

    def form_valid(self, form):
        book_title_page_link = form.cleaned_data['book_title_page_link']
        book_chapter_page_link = form.cleaned_data['book_chapter_page_link']

        website = form.save(commit=False)
        website_link = website.website_link

        parser = BookParser(website_link)
        name = get_website_name_from_link(website_link)
        icon_link = parser.get_website_icon_src()

        website.name = name
        website.icon_link = icon_link

        if book_title_page_link:
            website.book_title_page_length = get_book_title_page_length(
                book_title_page_link)
            if book_chapter_page_link:
                website.book_title_page_link_supplement = get_book_title_page_link_supplement(
                    book_title_page_link, book_chapter_page_link)

        website.save()

        return redirect(reverse_lazy('library:index-website'))


class WebsiteUpdateOneValView(generic.DetailView):
    model = Website
    template_name = 'libraryJ/update_website.html'
    context_object_name = 'website'

    def post(self, request, *args, **kwargs):
        website = self.get_object()
        book_description_path = request.POST.get('bookDescriptionPath')
        book_author_path = request.POST.get('bookAuthorPath')
        book_tags_path = request.POST.get('bookTagsPath')

        if book_description_path is not None:
            website.book_description_path = book_description_path

        if book_author_path is not None:
            website.book_author_path = book_author_path

        if book_tags_path is not None:
            website.book_tags_path = book_tags_path

        website.save()

        referer_url = request.META.get('HTTP_REFERER', None)

        return redirect(referer_url)


def get_Parser_Data(request, pk, path):
    website = get_object_or_404(Website, pk=pk)
    book = Book.objects.filter(Website=website).first()
    path = path.split(';')
    parser = BookParser(book.first_chapter_link)
    element = parser.get_element_by_path(parser._page_html, path)
    
    print(element)

    data = {
            'element': str(element)
        }
    return JsonResponse(data)