# coding=utf-8

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='question_author')
    likes = models.ManyToManyField(User)

    def __unicode__(self):
        return self.title

    def get_url(self):
        return reverse('single-question-view', kwargs={'qa_id': self.id})


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='answer_author')

    def __unicode__(self):
        # Вернуть первые 32 символа
        return self.text[:32]

    def get_url(self):
        return reverse('single-question-view', kwargs={'qa_id': self.question.id})
