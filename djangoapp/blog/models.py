from django.contrib.auth.models import User
from django.db import models
from utils.rands import slugify_new
class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
        default=None,
        blank=True,
        null=True,
        max_length=255,
    )
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name)
        return super().save(*args, **kwargs)
    def __str__(self) -> str:
        return self.name
class Category(models.Model):
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
        default=None,
        blank=True,
        null=True,
        max_length=255,
    )
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name)
            return super().save(*args, **kwargs)
    def __str__(self) -> str:
        return self.name
class Page(models.Model):
    title = models.CharField(max_length=65)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        default="",
        blank=True,
        null=True,
    )
    is_published = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisará estar marcado '
            'para a página ser exibida publicamente.'
        ),
    )
    content = models.TextField(default='')    
    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify_new(self.title)
            return super().save(*args, **kwargs)
    def __str__(self) -> str:
        return self.title
    
class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    title = models.CharField(max_length=65)
    excerpt = models.CharField(max_length=155)
    content = models.TextField()
    cover = models.ImageField(upload_to="posts/%Y/%m/", blank=True, default='')
    cover_in_post_content = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='post_created_by'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='post_updated_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, default='')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        blank=True,
        )
    is_published = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisará estar marcado '
            'para a página ser exibida publicamente.'
        ),
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        default='',
        null=True,
        blank=True
    )
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title)
        return super().save(*args, **kwargs)
            
    def __str__(self) -> str:
        return self.title