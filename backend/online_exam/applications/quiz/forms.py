from django import forms
from .models import Question, QuestionAnswer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['exam']


class QuestionAnswerForm(forms.ModelForm):
    class Meta:
        model = QuestionAnswer
        exclude = ['question']
