from django.views.generic import CreateView, ListView, DetailView
from applications.core.views import LoginRequiredMixin
from .forms import ExamForm
from .models import Exam


class ExamCreateView(CreateView):
    form_class = ExamForm


class ExamListView(LoginRequiredMixin, ListView):
    template_name = 'exam/list.html'
    model = Exam
    context_object_name = 'exams'

class ExamDetailView(DetailView):
    pass
