from django.conf.urls import url, include
from .views import ExamListView, ExamDetailView, ExamCreateView, \
    ExamDeleteView, TakeExamView
from applications.quiz import urls as question_urls

urlpatterns = [
    url('^$', ExamListView.as_view(), name='list'),
    url('^add/$', ExamCreateView.as_view(), name='add'),
    url('^(?P<pk>[^/]+)/$', ExamDetailView.as_view(), name='detail'),
    url('^(?P<pk>[^/]+)/delete/$', ExamDeleteView.as_view(), name='delete'),

    url('^(?P<pk>[^/]+)/questions/',
        include(question_urls, namespace='questions')),

    url('^(?P<pk>[^/s]+)/take/(?P<num>\d+)/$', TakeExamView.as_view(),
        name='take'),
]
