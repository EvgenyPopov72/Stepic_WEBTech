from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator

from qa.models import Question, Answer


def test(request, *args, **kwargs):
    return HttpResponse('testView')


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


@require_GET
def singleQuestions(request, qa_id):
    question = get_object_or_404(Question, id=qa_id)
    answers = Answer.objects.all().filter(question=question.id)
    return render_to_response('single-question-template.html', {'question': question, 'answers': answers})


def loginView(request, *args, **kwargs):
    return HttpResponse('loginView')


def registerView(request, *args, **kwargs):
    return HttpResponse('registerView')


def badRequest400(request):
    return render_to_response('errors.html', {'errorText': '400. OOoops. Something going wrong!'})


def pageNotFound404(request):
    return render_to_response('errors.html', {'errorText': '404. OOoops. Something going wrong!'})


def serverError500(request):
    return render(request, 'errors.html', {'errorText': '500. OOoops. Something going wrong!'})
