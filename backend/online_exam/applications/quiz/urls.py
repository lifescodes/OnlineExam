from django.conf.urls import url
from .views import QuestionCreateView, QuizCreateView

urlpatterns = [
    url(r'^add/$', QuestionCreateView.as_view(), name='add'),
    url(r'^create/$', QuizCreateView.as_view(), name='create'),
]
