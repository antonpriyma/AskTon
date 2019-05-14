from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.urls import reverse
from django.views.generic import CreateView
from pip._vendor.requests import auth

from AskMe.forms import UserChangingForm, CustomLoginForm, QuestionUploadForm, \
    CustomUserCreationForm, AnswerUploadForm
from .models import Question, Profile, Answer
from .models import Tag
from .paginate import paginate


def questions_list(request):
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


@login_required  # TODO:контроль логина
def edit_profile(request, pk):
    obj = get_object_or_404(Profile, username=pk)  # TODO:ИСПРАВИТЬ

    form = UserChangingForm(request.POST or None, instance=obj)

    if form.is_valid():
        obj = form.save(commit=False)

        obj.save()

        messages.success(request, "You successfully updated the prfile")

        return HttpResponseRedirect('/index')

    else:
        context = {'form': form}
        return render(request, 'register/accountSettings.html', context)


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


def question_question(request, question_id):
    if request.method == 'POST':
        form = AnswerUploadForm(data=request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('content')
            answer = Answer(content=content, questions=Question.list.get(pk=question_id), author=request.user)
            answer.save()
            return HttpResponseRedirect(str(question_id))
    elif request.method == 'GET':
        form = AnswerUploadForm
        return render(request, 'AskMe/question.html', {'question': Question.list.get(pk=question_id), 'form': form})


class ProfileLoginView(LoginView):
    template_name = 'register/Login.html'
    redirect_field_name = 'continue'
    form_class = CustomLoginForm
    redirect_url = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/index')
        self.redirect_url = self.request.GET.get(self.redirect_field_name)
        return super().dispatch(request, *args, **kwargs)


class ProfileLogoutView(LogoutView):
    redirect_field_name = 'continue'


class ProfileCreateView(CreateView):
    template_name = 'register/register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('questions_list')

    def form_valid(self, form):
        return super(ProfileCreateView, self).form_valid(form)


class QuestionUploadView(CreateView):
    template_name = 'AskMe/ask.html'
    form_class = QuestionUploadForm

    redirect_field_name = 'continue'

    def get_success_url(self):
        return reverse('question', kwargs={'question_id': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(QuestionUploadView, self).form_valid(form)

# class ProfileUpdateView(LoginRequiredMixin,UpdateView):
#     model = Profile
#     context_object_name = 'profile'
#     form_class = UserChangingForm
#     template_name = 'register/accountSettings.html'
#     redirect_field_name = 'continue'
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
