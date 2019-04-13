from django.shortcuts import render

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Question
from .models import Tag


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
    questions = Question.list.hot_questions()
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
    return render(request, 'register/Login.html', {})


def settings(request):
    return render(request, 'register/accountSettings.html', {})


def register(request):
    return render(request, 'register/register.html', {})


def test(request):
    return render(request, 'AskMe/test.html', {})


def paginate(request, objects_list):
    paginator = Paginator(objects_list, 3)
    return paginator
