# Generated by Django 2.0.7 on 2018-07-19 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_question_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='ans',
            field=models.CharField(default='', max_length=1),
        ),
    ]