from datetime import datetime
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from vanilla import CreateView, DeleteView, ListView, DetailView, TemplateView

from applications.core.functions import get_object_or_none
from applications.core.views import LoginRequiredMixin, TeacherRequiredMixin, \
    StudentRequiredMixin
from applications.quiz.models import Question, QuestionAnswerUser
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
        form.instance.duration = form.cleaned_data['duration'] * 60
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
    queryset = Exam.objects.all().select_related('user')

    def get_queryset(self):
        if not self.request.user.is_student():
            return Exam.objects.filter(user=self.request.user)
        return super().get_queryset()


class ExamDetailView(DetailView):
    template_name = 'exam/detail.html'
    model = Exam
    context_object_name = 'exam'

    def get_template_names(self):
        if self.request.user.is_teacher():
            return ['exam/detail-teacher.html']
        return super(ExamDetailView, self).get_template_names()


class ExamDeleteView(LoginRequiredMixin, TeacherRequiredMixin, DeleteView):
    model = Exam
    success_url = reverse_lazy('exams:list')

    def get(self, request, *args, **kwargs):
        return self.post(request)


class TakeExamView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = 'exam/take.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam_id'] = self.kwargs.get('pk')
        return context

    def get(self, request, *args, **kwargs):
        exam = self.get_exam()
        if exam.available \
                or (exam.available_start.now().date() <=
                    datetime.now().date() <=
                    exam.available_end.now().date()):
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(
            reverse_lazy('exams:detail',
                         kwargs={'pk': self.kwargs.get('pk')}))

    def get_exam(self):
        return Exam.objects.get(id=self.kwargs.get('pk'))


class ExamActionView(LoginRequiredMixin, StudentRequiredMixin, View):
    def get(self, request, pk):
        if self.request.GET.get('get_question'):
            position = self.request.GET.get('num')
            question = self.get_question(position, self.kwargs.get('pk'))
            answers = question.answers.all()
            sub_answers = [answers[i:i+2] for i in range(0, len(answers), 2)]
            return render(request, 'exam/question.html',
                          {'question': question,
                           'sub_answers': sub_answers})

    def post(self, request, pk):
        if self.request.POST.get('skip'):
            # TODO: add skipped question to session
            pass

        if self.request.POST.get('answer'):
            question_id = request.POST.get('question')
            question_answer = request.POST.get('question_answer')

            user_answer = get_object_or_none(QuestionAnswerUser,
                                             question_id=question_id,
                                             user=request.user)
            if user_answer:
                user_answer.choice_id = question_answer
                user_answer.save()
            else:
                QuestionAnswerUser.objects.create(question_id=question_id,
                                                  choice_id=question_answer,
                                                  user=request.user)

            return HttpResponse('success')

        if self.request.POST.get('finish'):
            # TODO: finsih exam, delete session
            pass

    def get_question(self, position, exam_id):
        return Question.objects.get(position=position, exam__id=exam_id)

# TODO:class ExamScoreView()
