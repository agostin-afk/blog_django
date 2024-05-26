from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post, PostManager
from django.db.models import Q

PER_PAGE = 9
def index(request):
    posts = Post.objects.get_is_published() # type: ignore
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

def created_by(request, author_pk):
    posts = Post.objects.get_is_published().filter(created_by__pk=author_pk) # type: ignore
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

def category(request, slug):
    posts = Post.objects.get_is_published().filter(category__slug=slug) # type: ignore
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def page(request, slug):

    return render(
        request,
        'blog/pages/page.html',
        {
            # 'page_obj': page_obj,
        }
    )


def post(request, slug):
    post = Post.objects.get_is_published().filter(slug=slug).first() # type: ignore
    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
        }
    )
    
def tags(request, slug):
    posts = Post.objects.get_is_published().filter(tags__slug=slug) # type: ignore
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
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
    # paginator = Paginator(posts, PER_PAGE)
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
        }
    )