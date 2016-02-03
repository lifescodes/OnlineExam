from django.conf.urls import url
from .views import QuestionCreateView, QuizCreateView, QuestionListView, \
    QuestionEditView

urlpatterns = [
    url(r'^$', QuestionListView.as_view(), name='list'),
    url(r'^add/$', QuestionCreateView.as_view(), name='add'),
    url(r'^create/$', QuizCreateView.as_view(), name='create'),
    url(r'^edit/$', QuestionEditView.as_view(), name='edit')
]
