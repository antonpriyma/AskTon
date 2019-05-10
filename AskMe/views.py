from django.shortcuts import render
from pip._vendor.requests import auth
import json

from .paginate import paginate
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Question
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Tag
from .models import User
from django import forms
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm


def questions_list(request):
    # return render(request, 'AskMe/index.html',{'questions':questions})
    questons = Question.list.all()
    paginator = paginate(request, questons)
    page = request.GET.get('page')
    try:
        quest = paginator.page(page)
    except PageNotAnInteger:
        quest = paginator.page(1)
    except EmptyPage:
        quest = paginator.page(paginator.num_pages)

    return render(request, 'AskMe/index.html', {'questions': quest})


def hot_list(request):
    # return render(request, 'AskMe/index.html',{'questions':questions})
    questions = Question.list.hot_questions()
    paginator = paginate(request, questions)
    page = request.GET.get('page')

    try:
        quest = paginator.page(page)
    except PageNotAnInteger:
        quest = paginator.page(1)
    except EmptyPage:
        quest = paginator.page(paginator.num_pages)

    return render(request, 'AskMe/hot.html', {'questions': quest})


def best_list(request):
    # return render(request, 'AskMe/index.html',{'questions':questions})
    questions = Question.list.best_questions()
    paginator = paginate(request, questions)
    page = request.GET.get('page')

    try:
        quest = paginator.page(page)
    except PageNotAnInteger:
        quest = paginator.page(1)
    except EmptyPage:
        quest = paginator.page(paginator.num_pages)

    return render(request, 'AskMe/best_questions.html', {'questions': quest})


def new_list(request):
    # return render(request, 'AskMe/index.html',{'questions':questions})
    questions = Question.list.new_questions()
    paginator = paginate(request, questions)
    page = request.GET.get('page')

    try:
        quest = paginator.page(page)
    except PageNotAnInteger:
        quest = paginator.page(1)
    except EmptyPage:
        quest = paginator.page(paginator.num_pages)

    return render(request, 'AskMe/new_questions.html', {'questions': quest})


def ask_question(request):
    return render(request, 'AskMe/ask.html', {})


def question_question(request, question_id):
    return render(request, 'AskMe/question.html', {'question': Question.list.get(pk=question_id)})


def tag_question(request, tag_name):
    tag = Tag.objects.get(text=tag_name)
    questions = Question.list.new_questions().filter(tags__text=tag.text)
    paginator = paginate(request, questions)
    page = request.GET.get('page')

    try:
        quest = paginator.page(page)
    except PageNotAnInteger:
        quest = paginator.page(1)
    except EmptyPage:
        quest = paginator.page(paginator.num_pages)
    return render(request, 'AskMe/QuestionsForTag.html', {'tag': tag, 'questions': quest})


def login(request):
    if (request.method == 'POST'):
        username=request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request,username=username,password=password)
        if user:
            auth.login(request,user)
            return HttpResponseRedirect('index')
        else:
            return HttpResponseRedirect('login/invalid')

    else:
        return render(request, 'register/Login.html')

def login_invalid(request):
    return render(request, 'register/Login.html', {'error':"Invalid login or password:("})


def settings(request):
    return render(request, 'register/accountSettings.html', {})


def register(request):
    form = UserCreationForm()
    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.create_user(username, email, password)
        user.save()
        HttpResponseRedirect('index')


    return render(request, 'register/register.html')

def logout(request):
    auth.logout(request)
    return questions_list(request)

def js(request):
    return render(request,'AskMe/empty_js_page.html')

def count(request):
    return JsonResponse({'count':'5'})


def test(request):
    return render(request, 'AskMe/test.html', {})


