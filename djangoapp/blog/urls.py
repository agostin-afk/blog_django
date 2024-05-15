from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from blog.views import index

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
]