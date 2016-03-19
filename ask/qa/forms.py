# coding=utf-8
from django import forms

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
        question.author_id = self._current_user_id
        question.save()
        return question

        # return Question.objects.create(**self.cleaned_data)

    def __init__(self, *args, **kwargs):
        self._current_user_id = kwargs.get('current_user_id')
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

    # def clean_question(self):
    #     question = self.cleaned_data['question']
    #     return question

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.author_id = self._current_user_id
        answer.save()
        return answer

    def __init__(self, *args, **kwargs):
        self._current_user_id = kwargs.get('current_user_id')
        if 'current_user_id' in kwargs:
            del kwargs['current_user_id']
        super(AnswerForm, self).__init__(*args, **kwargs)


def is_spam(text):
    '''
    Проверка на спам ))
    :param text:
    :return:
    '''
    if 'spam' in text.lower():
        return True
    return False
