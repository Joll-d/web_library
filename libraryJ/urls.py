from django.urls import path

from . import views

urlpatterns = [
    path('add-book/', views.AddBookView.as_view(), name='add'),
    path('add-book/post-book', views.AddBookView.as_view(), name='add'),
    path('add-website/post-website',
         views.WebsiteView.as_view(), name='post-website'),
    path('add-website/', views.WebsiteView.as_view(), name='post-website'),
    path('website/<int:pk>/update', views.WebsiteUpdateView.as_view(), name='website-update'),

    path('book/<int:pk>/', views.BookIndexView.as_view(), name='book-home-page'),
    path('book/<int:pk>/chapter/', views.BookPageView.as_view(), name='book-page'),
    path('book/<int:pk>/chapter/change-book-page',
         views.BookPageView.as_view(), name='change-book-page'),
    path('book/<int:pk>/delete', views.BookDeleteView.as_view(),
         name='delete-book-page'),

    path('', views.IndexView.as_view(), name='index'),
]
