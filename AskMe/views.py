from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Post

# Create your views here.
QUESTIONS = {

}

def questions_list(request):
    return render(request, 'AskMe/index.html',{})

def ask_question(request):
    return render(request,'AskMe/ask.html',{})


def question_question(request):
    return render(request,'AskMe/question.html',{})

def tag_question(request):
    return render(request,'AskMe/QuestionsForTag.html',{})

def login(request):
    return render(request,'register/Login.html',{})

def settings(request):
    return render(request,'register/accountSettings.html',{})

def register(request):
    return render(request,'register/register.html',{})

