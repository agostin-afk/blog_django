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