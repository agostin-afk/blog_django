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
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_is_published() # type: ignore
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     get_queryset = queryset.filter(is_published=True)
    #     return get_queryset
    
 
class CreatedByListView (PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username
        
        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name} -' 
        page_title= user_full_name + ' posts -'
        
        ctx.update({
            'page_title': page_title,
        })
        return ctx
    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        return qs

    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404()

        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })

        return super().get(request, *args, **kwargs)


class CategoryListView(PostListView):
    ...
    allow_empty = False
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        
        page_title = f'{self.object_list[0].category.name} - ' #type: ignore
        
        ctx.update({
            'page_title': page_title,
        })
        
        return ctx

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
    
class TagsListView(PostListView):
    ...
    allow_empty = False
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        
        page_title = f'{self.object_list[0].tags.first().name} - ' #type: ignore
        
        ctx.update({
            'page_title': page_title,
        })
        
        return ctx

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