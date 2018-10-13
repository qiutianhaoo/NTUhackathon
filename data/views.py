from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
import csv, io
from .models import Data
import requests
from django.http import JsonResponse
from . import Transcription
from . import PS_Rules

def random_sents(request):
    form = forms.Random()
    return render(request, 'data/random_sents.html', {'form': form})

def random_output(request):
    if request.method == "POST":
        form = forms.Random(request.POST)
        if form.is_valid():
            nouns = form.cleaned_data['nouns']
            verbs = form.cleaned_data['verbs']
            adj = form.cleaned_data['adj']
            prep = form.cleaned_data['prep']
            verbs_i = form.cleaned_data['verbs_i']
            adv = form.cleaned_data['adv']
            nouns = list(map(lambda x: (x,"",""), nouns.split()))
            verbs = list(map(lambda x: (x,"",""), verbs.split()))
            adj = list(map(lambda x: (x,"",""), adj.split()))
            prep = list(map(lambda x: (x,"",""), prep.split()))
            verbs_i = list(map(lambda x: (x,"",""), verbs_i.split()))
            adv = list(map(lambda x: (x,"",""), adv.split()))
            PS_Rules.nouns += (nouns)
            PS_Rules.verbs += (verbs)
            PS_Rules.verbs_i += (verbs_i)
            PS_Rules.adj += (adj)
            PS_Rules.adv += (adv)
            PS_Rules.prep += (prep)
            result = PS_Rules.run()
            return render(request, 'data/random_output.html', {'data': result})
    else:
        form = forms.Random()
    return render(request, 'data/random_output.html', {'data': ""})

def transliterate(request):
    if request.method == "POST":
        form = forms.Transliterate(request.POST)
        if form.is_valid():
            word = form.cleaned_data['text']
            src = int(form.cleaned_data['src'])
            dst = int(form.cleaned_data['dst'])
            #result = word
            result = Transcription.transcribe(word, src, dst)
            '''
            response = HttpResponse(content_type = 'text/csv')
            response['Content-Disposition'] = 'attachment; filename="output.csv"'

            data = [[result]]
            writer = csv.writer(response)
            for row in data:
                writer.writerow(row)
            return response
            '''
            return render(request, 'data/transliterate_output.html', {'data': result})
    else:
        form = forms.Transliterate()
    return render(request, 'data/transliterate.html', {'form': form})

def transliterate_output(request):
    return render(request, 'data/transliterate_output.html', {'data': ""})

def text_analyse(request):
    form = forms.LoadData()
    return render(request, 'data/analyse_text.html', {'form': form})

def text_csv(request):
        if request.method == "POST":
            form = forms.LoadData(request.POST)
            if form.is_valid():
                words = form.cleaned_data['text']
                response = HttpResponse(content_type = 'text/csv')
                response['Content-Disposition'] = 'attachment; filename="output.csv"'

                data = analyse_text_csv(words)
                #write("try.csv", data)
                writer = csv.writer(response)
                for row in data:
                    writer.writerow(row)
                return response
        else:
            form = forms.LoadData()
        return render(request, 'data/analyse_text.html', {'form': form})

def analyse_text_csv(words):
    dic = {}
    for word in words.split():
        if word not in dic:
            dic[word] = 0
        dic[word] += 1
    output = list(map(lambda t: list(t), dic.items()))
    output.sort(key = lambda x: x[1], reverse = True)
    return output

def js_test(request):
    form = forms.LoadData()
    return render(request, 'data/js_test.html', {'form': form})
    #return render(request, 'data/js_test.html', {"data": JsonResponse({"try": "hello"})})

def read_csv(fname):
    new = []
    with open(fname, encoding = 'utf-8') as f:
        for row in csv.reader(f):
            new.append(row)
    return new

def csv_view(request):
    if request.method == "POST":
        form = forms.LoadData(request.POST)
        if form.is_valid():
            words = form.cleaned_data['text']
            response = HttpResponse(content_type = 'text/csv')
            response['Content-Disposition'] = 'attachment; filename="output.csv"'

            #data = process_words(words)
            #write("try.csv", data)
            writer = csv.writer(response)
            for row in data:
                writer.writerow(row)
            return response
    else:
        form = forms.LoadData()
    return render(request, 'data/csv_view.html', {'form': form})

def csv_input(request):
    form = forms.LoadData()
    return render(request, 'data/data_input.html', {'form': form})

'''
def convert(request):
    currency = request.form.get("currency")
    res = requests.get("http://api.fixer.io/latest", params = { "base": "USD", "symbols": currency })

    if res.status_code != 200:
        return jsonify({"success": False})

    data = res.json()
    if currency not in data["rates"]:
        return jsonify({"success": False})
    else:
        return jsonify({"success": True, "rate": data["rates"][currency]})
'''
