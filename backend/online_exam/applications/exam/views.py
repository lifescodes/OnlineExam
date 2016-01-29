from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from vanilla import CreateView

from applications.core.views import LoginRequiredMixin
from .forms import ExamForm
from .models import Exam


class ExamCreateView(LoginRequiredMixin, CreateView):
    # form_class = ExamForm
    model = Exam
    template_name = 'exam/create.html'
    success_url = '/exams/'
    # fields = ('title', 'description', 'duration', 'difficulty',
    #           'available', 'available_start', 'available_end')

    def get(self, request, *args, **kwargs):
        if request.user.is_student():
            return HttpResponseRedirect(reverse('exams:list'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.cleaned_data['user'] = self.request.user
        super().form_valid(form)


class ExamListView(LoginRequiredMixin, ListView):
    template_name = 'exam/list.html'
    context_object_name = 'exams'
    model = Exam

    def get_queryset(self):
        if self.request.user.is_teacher():
            return Exam.objects.filter(user=self.request.user)
        super().get_queryset()


class ExamDetailView(DetailView):
    template_name = 'exam/detail.html'
    model = Exam
    context_object_name = 'exam'
