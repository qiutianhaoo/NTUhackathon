# Generated by Django 2.0.6 on 2018-06-16 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='thumbnail',
        ),
    ]
