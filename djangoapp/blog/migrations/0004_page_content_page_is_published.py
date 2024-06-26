# Generated by Django 5.0.6 on 2024-05-19 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='page',
            name='is_published',
            field=models.BooleanField(default=False, help_text='Este campo precisará estar marcado para a página ser exibida publicamente.'),
        ),
    ]
