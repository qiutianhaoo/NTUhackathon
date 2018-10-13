from django.shortcuts import render, redirect
from .models import Article
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
import csv
# Create your views here.
def article_list(request):
    articles = Article.objects.all().order_by("date")
    return render(request, 'articles/article_list.html', {'articles':articles})

def article_detail(request, slug):
    #return HttpResponse(slug)
    article = Article.objects.get(slug = slug)
    return render(request, 'articles/article_detail.html', {'article': article})

@login_required(login_url = "/accounts/login/")
def article_create(request):
    if request.method == "POST":
        form = forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            # save article to db
            return redirect('articles:list')
    else:
        form = forms.CreateArticle()
    return render(request, 'articles/article_create.html', {'form': form})

def read_csv(fname):
    new = []
    with open(fname, encoding = 'utf-8') as f:
        for row in csv.reader(f):
            new.append(row)
    return new

def csv_view(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename="test.csv"'

    data = read_csv("test.csv")
    writer = csv.writer(response)
    for row in data:
        writer.writerow(data)
    return response
