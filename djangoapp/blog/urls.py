from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from blog.views import PostListView, page, post, CreatedByListView, CategoryListView, tags, search

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('page/', page, name='page'),
    path('post/<slug:slug>/', post, name='post'),
    path('created_by/<int:author_pk>/', CreatedByListView.as_view(), name='created_by'),
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category'),
    path('tags/<slug:slug>/', tags, name='tag'),
    path('search/', search, name='search'),
    
]