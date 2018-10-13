#from django.contrib import admin
from django.urls import path, re_path
from . import views

app_name = "quiz"

urlpatterns = [
    re_path(r'^(?P<number>[\w-]+)/$', views.question, name = 'quiz'),
]
