from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from vanilla import CreateView, DeleteView, ListView, DetailView, TemplateView

from applications.core.views import LoginRequiredMixin, TeacherRequiredMixin, \
    StudentRequiredMixin
from .forms import ExamForm
from .models import Exam


class ExamCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    form_class = ExamForm
    template_name = 'exam/new.html'
    success_url = '/exams/'

    def get(self, request, *args, **kwargs):
        if request.user.is_student():
            return HttpResponseRedirect(reverse_lazy('exams:list'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.POST.get('add_questions'):
            return reverse_lazy('questions:new')
        return super().get_success_url()


class ExamListView(LoginRequiredMixin, ListView):
    template_name = 'exam/list.html'
    context_object_name = 'exams'
    model = Exam

    def get_queryset(self):
        if not self.request.user.is_student():
            return self.model.objects.filter(user=self.request.user)
        return super().get_queryset()


class ExamDetailView(DetailView):
    template_name = 'exam/detail.html'
    model = Exam
    context_object_name = 'exam'


class ExamDeleteView(LoginRequiredMixin, TeacherRequiredMixin, DeleteView):
    model = Exam
    success_url = reverse_lazy('exams:list')

    def get(self, request, *args, **kwargs):
        return self.post(request)


class TakeExamView(LoginRequiredMixin, StudentRequiredMixin,TemplateView):
    template_name = 'exam/take.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam'] = Exam.objects.get(id=self.kwargs.get('pk'))
        return context
