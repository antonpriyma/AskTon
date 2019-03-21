from django.urls import path
from . import views


urlpatterns = [
    path('', views.questions_list, name='questions_list'),
    path('questions', views.questions_list, name='questions_list'),
    path('ask', views.ask_question, name='ask_question'),
    path('question', views.question_question, name='question'),
    path('tag', views.tag_question, name='tag'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('settings', views.settings, name='settings'),

]