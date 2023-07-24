from django.urls import path

from . import views

app_name = 'library'

urlpatterns = [
    path('website/create',
         views.WebsiteCreateView.as_view(), name='create-website'),
    path('website/', views.WebsiteView.as_view(), name='index-website'),
    path('website/<int:pk>/update',
         views.WebsiteUpdateView.as_view(), name='update-website'),
    path('website/<int:pk>/update-one-val',
         views.WebsiteUpdateOneValView.as_view(), name='update-one-val-website'),

    path('book/create/', views.BookCreateView.as_view(), name='create-book'),
    path('book/<int:pk>/', views.BookIndexView.as_view(), name='index-book'),
    path('book/<int:pk>/update', views.BookUpdateView.as_view(), name='update-book'),
    path('book/<int:pk>/delete', views.BookDeleteView.as_view(),
         name='delete-book'),
         
    path('book/<int:pk>/chapter/', views.BookPageView.as_view(), name='book-page'),
    path('book/<int:pk>/chapter/change-book-page',
         views.BookPageView.as_view(), name='change-book-page'),

    path('', views.IndexView.as_view(), name='index-library'),
]
