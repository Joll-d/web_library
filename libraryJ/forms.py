from django import forms
from .models import *
from libraryJ.utils.parser import *
from libraryJ.utils.utils import *


class WebsiteCreateExtraFields(forms.Form):

    book_title_page_link = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    book_chapter_page_link = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))


class WebsiteCreateForm(forms.ModelForm, WebsiteCreateExtraFields):

    class Meta:
        model = Website
        fields = ['name', 'website_link', 'book_title_page_link_supplement',
                  'book_image_path', 'icon_link', 'book_title_path',
                  'chapter_title_path', 'book_content_path', 'next_chapter_link_path', 'previous_chapter_link_path',
                  'book_title_page_length']
        widgets = {
            'website_link': forms.TextInput(attrs={'class': 'form-control'}),

            'book_image_path': forms.TextInput(attrs={'class': 'form-control'}),
            'book_title_path': forms.TextInput(attrs={'class': 'form-control'}),
            'chapter_title_path': forms.TextInput(attrs={'class': 'form-control'}),
            'book_content_path': forms.TextInput(attrs={'class': 'form-control'}),
            'next_chapter_link_path': forms.TextInput(attrs={'class': 'form-control'}),
            'previous_chapter_link_path': forms.TextInput(attrs={'class': 'form-control'}),

            'name': forms.HiddenInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'value': 'None'}),
            'book_title_page_link_supplement': forms.HiddenInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'value': 'None'}),
            'icon_link': forms.HiddenInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'value': 'None'}),
            'book_title_page_length': forms.HiddenInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'value': 0}),
        }


class WebsiteUpdateExtraFields(forms.Form):

    book_title_page_link = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False)
    book_chapter_page_link = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False)


class WebsiteUpdateForm(forms.ModelForm, WebsiteUpdateExtraFields):
    def __init__(self, *args, **kwargs):
        super(WebsiteUpdateForm, self).__init__(*args, **kwargs)
        self.fields['book_tags_path'].required = False
        self.fields['book_author_path'].required = False
        self.fields['book_description_path'].required = False
        self.fields['book_title_page_link_supplement'].required = False

        self.fields['book_title_path'].widget.attrs['onclick'] = 'getPreviewData(this.value)'
        self.fields['chapter_title_path'].widget.attrs['onclick'] = 'getPreviewData(this.value)'
        self.fields['book_content_path'].widget.attrs['onclick'] = 'getPreviewData(this.value)'
        self.fields['next_chapter_link_path'].widget.attrs['onclick'] = 'getPreviewData(this.value)'
        self.fields['previous_chapter_link_path'].widget.attrs['onclick'] = 'getPreviewData(this.value)'
        self.fields['book_image_path'].widget.attrs['onclick'] = 'getPreviewData(this.value)'

    class Meta:
        model = Website
        fields = ['name', 'website_link', 'icon_link',
                  'book_title_page_length', 'book_title_page_link_supplement',
                  'book_tags_path', 'book_description_path',
                  'book_author_path', 'book_image_path', 'book_title_path',
                  'chapter_title_path', 'book_content_path', 'next_chapter_link_path', 'previous_chapter_link_path']
        widgets = {
            'website_link': forms.TextInput(attrs={'class': 'form-control'}),

            'book_tags_path': forms.TextInput(attrs={'class': 'form-control', 'value': ''}),
            'book_description_path': forms.TextInput(attrs={'class': 'form-control', 'value': ''}),
            'book_author_path': forms.TextInput(attrs={'class': 'form-control', 'value': ''}),
            'book_image_path': forms.TextInput(attrs={'class': 'form-control'}),

            'book_title_path': forms.TextInput(attrs={'class': 'form-control'}),
            'chapter_title_path': forms.TextInput(attrs={'class': 'form-control'}),
            'book_content_path': forms.TextInput(attrs={'class': 'form-control'}),
            'next_chapter_link_path': forms.TextInput(attrs={'class': 'form-control'}),
            'previous_chapter_link_path': forms.TextInput(attrs={'class': 'form-control'}),

            'name': forms.HiddenInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'book_title_page_link_supplement': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'icon_link': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'book_title_page_length': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }


class BookCreateForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['first_chapter_link']
        widgets = {
            'first_chapter_link': forms.TextInput(attrs={'class': 'form-control'}),
        }