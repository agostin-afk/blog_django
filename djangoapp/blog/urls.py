from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from blog.views import index, page, post

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('page/', page, name='page'),
    path('post/<slug:slug>/', post, name='post'),
]