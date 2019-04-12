from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Post

# Create your views here.
userDanya =({'photo': 'images/сool_programmer.jpg', 'name':'Gaver'})
userSanya =({'photo': 'images/female_programmer.jpg', 'name':'SanyaChelaba'})
tags = []
tags.append({'text': "Heap"})
tags.append({'text': "C++"})
tags.append({'text': "Java"})
tags.append({'text': "Golang"})
tags.append({'text': "Python"})
questions = []
answers = []
for i in range(1,3):
    answers.append({
          'id': i,
          'rate': i,
          'title': "title " + str(i),
          'content': "text " + str(i),
          'author': userDanya
      })
for i in range(1,10):
  questions.append({
    'id': i,
    'rate': i,
   'title':"title " + str(i),
   'content': "text " + str(i),
    'tags': tags,
    'author': userDanya,
    'answers':answers
  })


questions.append({
'id': i,
   'title':"How to install linux and start living",
   'content': "text " + str(i),
    'tags': tags,
    'author': userSanya
})


def questions_list(request):
    # return render(request, 'AskMe/index.html',{'questions':questions})
    paginator=paginate(request)
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
    paginator = paginate(request)
    page = request.GET.get('page')

    try:
        quest = paginator.page(page)
    except PageNotAnInteger:
        quest = paginator.page(1)
    except EmptyPage:
        quest = paginator.page(paginator.num_pages)

    return render(request, 'AskMe/hot.html', {'questions': quest})


def ask_question(request):
    return render(request,'AskMe/ask.html',{})


def question_question(request,question_id):
    return render(request,'AskMe/question.html',{'id': question_id,'question': questions[int(question_id)],'answers': questions[:3]})

def tag_question(request,tag_name):
    if (tag_name):
        tag = ({'text': tag_name})
    return render(request,'AskMe/QuestionsForTag.html',{'tag':tag,'questions':questions})

def login(request):
    return render(request,'register/Login.html',{})

def settings(request):
    return render(request,'register/accountSettings.html',{})

def register(request):
    return render(request,'register/register.html',{})

def test(request):
    return render(request,'AskMe/test.html',{})

# def paginate(objects_list, request):
#     paginator = Paginator(objects_list,4)
#     page = request.GET.get("")
#     questions_paginate = page.get_page(page)
#     return objects_page, paginator



def paginate(request):
    paginator = Paginator(questions, 3)
    return paginator
    # page = request.GET.get('page')
    #
    # try:
    #     quest = paginator.page(page)
    # except PageNotAnInteger:
    #     quest = paginator.page(1)
    # except EmptyPage:
    #     quest = paginator.page(paginator.num_pages)
    #
    # return render(request, 'AskMe/index.html', {'questions': quest})


