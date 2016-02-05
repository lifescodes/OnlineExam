from django.conf.urls import url
from .views import QuestionCreateView, QuizCreateView, QuestionListView, \
    QuestionEditView, QuestionDeleteView

urlpatterns = [
    url(r'^$', QuestionListView.as_view(), name='list'),
    url(r'^add/$', QuestionCreateView.as_view(), name='add'),
    url(r'^create/$', QuizCreateView.as_view(), name='create'),
    url(r'^edit/$', QuestionEditView.as_view(), name='edit'),
    url(r'^(?P<question_id>\d+)/delete/$', QuestionDeleteView.as_view(),
        name='delete')
]
