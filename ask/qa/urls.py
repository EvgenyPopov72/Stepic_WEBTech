from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^question/(?P<qa_id>\d+)/$', views.test),
    url(r'^question/', views.test),
    url(r'^login/', views.test),
    url(r'^signup/', views.test),
    url(r'^ask/', views.test),
    url(r'^popular/', views.test),
    url(r'^new/', views.test),
    url(r'^$', views.test),
]
