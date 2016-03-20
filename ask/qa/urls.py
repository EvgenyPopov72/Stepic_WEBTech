# coding=utf-8
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^question/(?P<qa_id>\d+)/$', views.singleQuestion, name='single-question-view'),
    url(r'^question/', views.singleQuestion, kwargs={'qa_id': 1}, name='single-question-view'),

    # url(r'^answer/', views.answerView, name='answer-view'),
    url(r'^answer/', views.singleQuestion, kwargs={'qa_id': -1}, name='answer-view'),

    url(r'^login/', views.loginView, name='login-view'),
    url(r'^logout/', views.logoutView, name='logout-view'),
    url(r'^signup/', views.signupView, name='signup-view'),

    url(r'^ask/', views.askView, name='ask-view'),
    url(r'^popular/', views.popularQuestions, name='popular-question-view'),
    url(r'^new/', views.test),
    url(r'^$', views.lastQuestions, name='last-question-view'),
]
