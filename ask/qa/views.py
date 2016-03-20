# coding=utf-8
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator
from django.views.defaults import bad_request

from qa.forms import AskForm, AnswerForm, LoginForm, SignupForm
from qa.models import Question, Answer


def test(request, *args, **kwargs):
    # return HttpResponse('testView')
    return request.redirect('/new_url/')


@require_GET
def popularQuestions(request, *args, **kwargs):
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 100
    questions = Question.objects.order_by('-rating').all()[:]
    paginator = Paginator(questions, limit)
    paginator.baseurl = reverse('popular-question-view') + '?page='
    page = paginator.page(page)  # Page
    return render(request, 'popular-question-template.html',
                  {'page': page,
                   'questions': page.object_list,
                   'paginator': paginator})


@require_GET
def lastQuestions(request, *args, **kwargs):
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 100
    questions = Question.objects.order_by('-id').all()[:]
    paginator = Paginator(questions, limit)
    paginator.baseurl = reverse('last-question-view') + '?page='
    page = paginator.page(page)  # Page
    return render(request, 'last-question-template.html',
                  {'page': page,
                   'questions': page.object_list,
                   'paginator': paginator})


def singleQuestion(request, qa_id):
    current_user_id = None
    if qa_id == -1:
        qa_id = request.POST.get('question', -1)
        if qa_id == -1:
            # raise badRequest400()
            return HttpResponseRedirect('/')
    if request.user.is_authenticated():
        current_user_id = request.user.id
    question = get_object_or_404(Question, id=qa_id)
    answers = Answer.objects.all().filter(question=question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, current_user_id=current_user_id)
        if form.is_valid():
            post = form.save()
            url = post.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question': question}, current_user_id=current_user_id)

    return render(request, 'single-question-template.html',
                  {'question': question, 'answers': answers, 'form': form})


def loginView(request, *args, **kwargs):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                form = LoginForm()
                form.non_field_errors = ['Пользователь заблокирован']
            else:
                form = LoginForm()
                form.non_field_errors = ['Неверные учетные данные']
    else:
        form = LoginForm()

    return render(request, 'login-signup-template.html', {'form': form, 'title': 'Login', 'signup': False})


def logoutView(request, *args, **kwargs):
    logout(request)
    return HttpResponseRedirect("/")


def signupView(request, *args, **kwargs):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            user = User.objects.create_user(username=username, email=email, password=password)
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignupForm()

    return render(request, 'login-signup-template.html', {'form': form, 'title': 'Signup', 'signup': True})


def askView(request, *args, **kwargs):
    current_user_id = None
    if request.user.is_authenticated():
        current_user_id = request.user.id
    if request.method == "POST":
        form = AskForm(request.POST, current_user_id=current_user_id)
        if form.is_valid():
            post = form.save()
            url = post.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm(current_user_id=current_user_id)
    return render(request, 'ask-template.html', {'form': form})


def badRequest400(request):
    return render_to_response('errors.html', {'errorText': '400. OOoops. Something going wrong!'})


def pageNotFound404(request):
    return render_to_response('errors.html', {'errorText': '404. OOoops. Something going wrong!'})


def serverError500(request):
    return render(request, 'errors.html', {'errorText': '500. OOoops. Something going wrong!'})
