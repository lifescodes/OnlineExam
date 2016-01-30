from django.conf.urls import url, include
from .views import ExamListView, ExamDetailView, ExamCreateView, ExamDeleteView
from applications.quiz import urls as question_urls

urlpatterns = [
    url('^$', ExamListView.as_view(), name='list'),
    url('^add/$', ExamCreateView.as_view(), name='add'),
    url('^v/(?P<pk>[^/]+)$', ExamDetailView.as_view(), name='detail'),
    url('^v/(?P<pk>[^/]+)/delete/$', ExamDeleteView.as_view(), name='delete'),

    url('^v/(?P<pk>[^/]+)/questions/',
        include(question_urls, namespace='questions'))
]
