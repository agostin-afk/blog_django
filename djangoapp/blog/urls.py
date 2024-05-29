from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from blog.views import PostListView, PageDetailView, PostDetailView, CreatedByListView, CategoryListView, TagsListView, SearchListView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('page/', PageDetailView.as_view(), name='page'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post'),
    path('created_by/<int:author_pk>/', CreatedByListView.as_view(), name='created_by'),
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category'),
    path('tags/<slug:slug>/', TagsListView.as_view(), name='tag'),
    path('search/', SearchListView.as_view(), name='search'),
    
]