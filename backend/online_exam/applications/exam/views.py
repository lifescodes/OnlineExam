from django.views.generic import CreateView
from .forms import ExamForm


class ExamCreateView(CreateView):
    form_class = ExamForm
