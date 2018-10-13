from django.shortcuts import render
from .models import Question

# Create your views here.
def question(request, number):
    quiz = Question.objects.get(number = number)
    return render(request, 'quiz/question.html', {'quiz': quiz})
