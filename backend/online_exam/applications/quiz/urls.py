from django.conf.urls import url
from .views import QuestionCreateView


urlpatterns = [
    url(r'^add/$', QuestionCreateView.as_view(), name='add'),
]
