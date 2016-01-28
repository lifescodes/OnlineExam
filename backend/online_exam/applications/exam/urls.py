from django.conf.urls import url
from .views import ExamListView, ExamDetailView

urlpatterns = [
    url('^$', ExamListView.as_view(), name='list'),
    url('^(?P<pk>^\)$', ExamDetailView.as_view(), name='detail')
]
