# coding=utf-8
from django import forms
from django.contrib.auth.models import User

from qa.models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=100,
                            widget=forms.TextInput(
                                attrs={'placeholder': 'Enter title of the question', 'class': 'form-control'}))
    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter your question.', 'class': 'form-control'}))

    # def clean(self):
    #     pass

    def clean_title(self):
        title = self.cleaned_data['title']
        if is_spam(title):
            raise forms.ValidationError(u'Сообщение похоже на спам', code='spam')
        if len(title) > 100:
            raise forms.ValidationError(u'Длина заголовка должна составлять не более 100 символов')
        return title

    def clean_text(self):
        text = self.cleaned_data['text']
        if is_spam(text):
            raise forms.ValidationError(u'Сообщение похоже на спам', code='spam')
        return text

    def save(self):
        question = Question(**self.cleaned_data)
        if self._current_user_id:
            question.author_id = self._current_user_id
        question.save()
        return question

        # return Question.objects.create(**self.cleaned_data)

    def __init__(self, *args, **kwargs):
        self._current_user_id = kwargs.get('current_user_id', None)
        if 'current_user_id' in kwargs:
            del kwargs['current_user_id']
        super(AskForm, self).__init__(*args, **kwargs)


class AnswerForm(forms.Form):
    text = forms.CharField(max_length=100, label='Answer', widget=forms.Textarea(
        attrs={'placeholder': 'Enter your question.', 'class': 'form-control'}))
    question = forms.ModelChoiceField(queryset=Question.objects.all(), widget=forms.HiddenInput(), label='')

    # def clean(self):
    #     pass

    def clean_text(self):
        text = self.cleaned_data['text']
        if is_spam(text):
            raise forms.ValidationError(u'Сообщение похоже на спам', code='spam')
        if len(text) > 100:
            raise forms.ValidationError(u'Длина заголовка должна составлять не более 100 символов')
        return text

    def save(self):
        answer = Answer(**self.cleaned_data)
        if self._current_user_id:
            answer.author_id = self._current_user_id
        answer.save()
        return answer

    def __init__(self, *args, **kwargs):
        self._current_user_id = kwargs.get('current_user_id', None)
        if 'current_user_id' in kwargs:
            del kwargs['current_user_id']
        super(AnswerForm, self).__init__(*args, **kwargs)


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter username', 'class': 'form-control'}))  # - имя пользователя, логин
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter password', 'class': 'form-control'}))  # - пароль пользователя


class SignupForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter username', 'class': 'form-control'}))  # - имя пользователя, логин
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'Enter email', 'class': 'form-control'}))  # - email пользователя
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter password', 'class': 'form-control'}))  # - пароль пользователя

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=username).all() or User.objects.filter(email=email).all():
            raise forms.ValidationError(u'Такой пользователь уже существует')


def is_spam(text):
    '''
    Проверка на спам ))
    :param text:
    :return:
    '''
    if 'spam' in text.lower():
        return True
    return False
