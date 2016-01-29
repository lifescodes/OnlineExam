from django.conf.urls import url
from .views import ExamListView, ExamDetailView, ExamCreateView

urlpatterns = [
    url('^$', ExamListView.as_view(), name='list'),
    url('^add/$', ExamCreateView.as_view(), name='add'),
    url('^v/(?P<pk>[^/]+)$', ExamDetailView.as_view(), name='detail')
]
