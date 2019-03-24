from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Post

# Create your views here.
userDanya =({'photo': 'images/сool_programmer.jpg'})
userSanya =({'photo': 'images/female_programmer.jpg'})
tags = []
tags.append({'text': "Heap"})
tags.append({'text': "C++"})
tags.append({'text': "Java"})
tags.append({'text': "Golang"})
tags.append({'text': "Python"})
questions = []
for i in range(1,3):
  questions.append({
    'id': i,
   'title':"title " + str(i),
   'content': "text " + str(i),
    'tags': tags,
    'author': userDanya
  })

questions.append({
'id': i,
   'title':"How to install linux and start living",
   'content': "text " + str(i),
    'tags': tags,
    'author': userSanya
})


def questions_list(request):
    return render(request, 'AskMe/index.html',{'questions':questions})

def ask_question(request):
    return render(request,'AskMe/ask.html',{})


def question_question(request,question_id):
    return render(request,'AskMe/question.html',{'id': question_id,'question': questions[int(question_id)]})

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

