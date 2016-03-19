# coding=utf-8
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator
from django.views.defaults import bad_request

from qa.forms import AskForm, AnswerForm
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
    if qa_id == -1:
        qa_id = request.POST.get('question', -1)
        if qa_id == -1:
            # raise badRequest400()
            return HttpResponseRedirect('/')
    current_user_id = 1
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
    return HttpResponse('loginView')


def registerView(request, *args, **kwargs):
    return HttpResponse('registerView')


def askView(request, *args, **kwargs):
    # current_user = User.objects.filter(id=1).get()  # для простоты текущий юзер - первый юзер из базы
    current_user_id = 1
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
