from django.urls import include,path

from . import views


urlpatterns = [
    path('index/', views.questions_list, name='questions_list'),
    path('hot/', views.hot_list, name='hot_list'),
    path('ask', views.ask_question, name='ask_question'),
    path('question/<int:question_id>', views.question_question, name='question'),
    path('tag/<tag_name>', views.tag_question, name='tag'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('settings', views.settings, name='settings'),
    path('test/<page_num>', views.paginate, name='testPaginate'),
]

