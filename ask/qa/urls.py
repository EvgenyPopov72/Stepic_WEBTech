from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^question/(?P<qa_id>\d+)/$', views.singleQuestions),
    url(r'^question/', views.singleQuestions, name='single-question-view'),
    url(r'^login/', views.test, name='login-view'),
    url(r'^signup/', views.test, name='signup-view'),
    url(r'^ask/', views.test, name='ask-view'),
    url(r'^popular/', views.popularQuestions, name='popular-question-view'),
    url(r'^new/', views.test),
    url(r'^$', views.lastQuestions, name='last-question-view'),
]
