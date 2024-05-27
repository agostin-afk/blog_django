from typing import Any
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import render
from blog.models import Post, PostManager, Page
from django.contrib.auth.models import User
from django.http import Http404
from django.db.models import Q
from django.views.generic import ListView

PER_PAGE = 9

class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    ordering = '-pk',
    paginate_by = PER_PAGE
    queryset = Post.objects.get_is_published() # type: ignore
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     get_queryset = queryset.filter(is_published=True)
    #     return get_queryset
    
    
# def index(request):
#     posts = Post.objects.get_is_published() # type: ignore
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': 'Home - ',
#         }
#     )

def created_by(request, author_pk):
    user = User.objects.filter(pk=author_pk).first()
    if user is None:
        raise Http404()
    posts = Post.objects.get_is_published().filter(created_by__pk=author_pk) # type: ignore
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    user_full_name =user.username 
    if user.first_name:
        user_full_name = f'{user.first_name} {user.last_name} -' 
    page_title= user_full_name + ' posts -'
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
            
        }
    )

def category(request, slug):
    posts = Post.objects.get_is_published().filter(category__slug=slug) # type: ignore
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()
    page_title = f'{page_obj[0].category.name} - '
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


def page(request, slug):
    page_obj = Page.objects.filter(is_published=True).filter(slug=slug).first() # type: ignore
    if page_obj is None:
        raise Http404()
    page_title = f'{page_obj.title} - '
    return render(
        request,
        'blog/pages/page.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
            
        }
    )


def post(request, slug):
    post_obj = Post.objects.get_is_published().filter(slug=slug).first() # type: ignore
    if post_obj is None:
        raise Http404()
    page_title = f'{post_obj.title} - '
    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'page_title': page_title,
        }
    )
    
def tags(request, slug):
    posts = Post.objects.get_is_published().filter(tags__slug=slug) # type: ignore
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if len(page_obj) == 0:
        raise Http404()
    page_title = f'{page_obj[0].tags.first().name} - '
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
            
        }
    )

def search(request):
    search_value = request.GET.get('search').strip()
    posts = (
        Post.objects.get_is_published().filter( # type: ignore
            Q(title__icontains = search_value) |
            Q(excerpt__icontains = search_value) |
            Q(content__icontains = search_value)
        )[0:PER_PAGE]
    )

    page_title = f'{search_value[:30]} - '
    # paginator = Paginator(posts, PER_PAGE)
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
            'page_title': page_title,
            
        }
    )