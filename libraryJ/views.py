from django.urls import reverse_lazy
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
from django.contrib import messages
from django.utils import timezone
from .forms import *


class IndexView(generic.ListView):
    template_name = 'libraryJ/index.html'
    context_object_name = 'books'

    def get_queryset(self):

        return Book.objects.all().order_by('-last_call_time')


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

            book = Book.objects.create(
                Website=website,
                title=title,
                first_chapter_link=first_chapter_link,
                last_chapter_link=first_chapter_link,
                image_link=image_link,

                author=author,
                tags=tags,
                description=description,
            )
            return redirect(reverse_lazy('library:index-library'))


class BookIndexView(generic.DetailView):
    model = Book
    template_name = 'libraryJ/book_home_page.html'
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


class BookDeleteView(generic.DetailView):
    model = Book
    success_url = '../'

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        confirmation = request.POST.get('deleteConfirmation')
        if confirmation == 'I am sure':
            book.delete()

        return redirect('../../')


class BookUpdateView(generic.DetailView):
    model = Book
    fields = ["book_title", "art_link", "author", "tags", "description"]
    template_name = "libraryJ/book_home_page.html"

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


class BookPageView(generic.DetailView):
    model = Book
    template_name = 'libraryJ/book_page.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        chapter_link = book.last_chapter_link
        website = book.Website

        parser = BookParser(chapter_link)
        chapter_title = parser.get_element_text(website.chapter_title_path)
        chapter_content = parser.get_elements_text(website.book_content_path)

        previous_chapter = parser.get_element_href(
            website.previous_chapter_link_path)
        next_chapter = parser.get_element_href(
            website.next_chapter_link_path)

        translator_en = Translator('en')
        chapter_title_en = translator_en.translate(chapter_title)
        chapter_content_en = translator_en.translate(chapter_content)

        translator_ru = Translator('ru')

        chapter_content_ru = translator_ru.translate(chapter_content)

        context['chapter_title'] = chapter_title_en
        context['chapter_content'] = zip(
            chapter_content_en, chapter_content_ru)

        context['previous_chapter'] = previous_chapter
        context['next_chapter'] = next_chapter

        book.last_call_time = timezone.now()
        book.save()

        return context

    def post(self, request, *args, **kwargs):
        book = self.get_object()

        book_link = request.POST.get("next_chapter")

        if book_link != 'None':
            book.last_page_link = book_link
            book.save()

        return redirect(f"../chapter")


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


# class WebsiteUpdateView(generic.UpdateView, generic.DeleteView):
#     model = Website
#     form_class = WebsiteUpdateForm
#     template_name = 'libraryJ/update_website.html'
#     context_object_name = 'website'

#     def post(self, request, *args, **kwargs):
#         website = self.get_object()
#         book_description_path = request.POST.get('bookDescriptionPath')
#         book_author_path = request.POST.get('bookAuthorPath')
#         book_tags_path = request.POST.get('bookTagsPath')

#         if book_description_path is not None:
#             website.book_description_path = book_description_path

#         if book_author_path is not None:
#             website.book_author_path = book_author_path

#         if book_tags_path is not None:
#             website.book_tags_path = book_tags_path

#         website.save()

#         referer_url = request.META.get('HTTP_REFERER', None)

#         return redirect(referer_url)
