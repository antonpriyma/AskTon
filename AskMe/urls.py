from django.conf.urls.static import static
from django.urls import include,path
from django.contrib.auth.decorators import login_required, permission_required

from myproject import settings
from . import views


urlpatterns = [
    path('index/', views.questions_list, name='questions_list'),
    path('hot/', views.hot_list, name='hot_list'),
    path('best/', views.best_list, name='best_list'),
    path('new/', views.new_list, name='new_list'),
    path('ask', login_required(views.QuestionUploadView.as_view()), name='ask_question'),
    path('question/<int:question_id>', views.question_question, name='question'),
    path('tag/<tag_name>', views.tag_question, name='tag'),
    path('login/', views.ProfileLoginView.as_view(), name='login'),
    path('register', views.ProfileCreateView.as_view(), name='register'),
    path('settings/<pk>', views.edit_profile, name='settings'),
    path('logout', login_required(views.ProfileLogoutView.as_view()), name='logout'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

