from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.views.generic import View
from vanilla import CreateView, TemplateView, ListView, DeleteView

from applications.core.views import TeacherRequiredMixin, LoginRequiredMixin
from applications.quiz.models import Question, QuestionAnswer
from .forms import QuestionForm


class QuestionCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    form_class = QuestionForm
    template_name = 'quiz/new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam_id'] = self.kwargs.get('pk')
        return context


class QuizCreateView(LoginRequiredMixin, TeacherRequiredMixin, TemplateView):
    template_name = 'quiz/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam_id'] = self.kwargs.get('pk')
        context['current_number'] = self.get_last_number() + 1
        return context

    def get_last_number(self):
        q = Question.objects.filter(exam__id=self.kwargs.get('pk')).last()
        if not q:
            return 0
        return q.position

    def post(self, request, *args, **kwargs):
        question_text = request.POST.get('question')
        multiple = 2 if request.POST.get('multiple') else 1
        position = request.POST.get('position')

        question = Question.objects.create(text=question_text,
                                           question_type=multiple,
                                           position=position,
                                           exam_id=request.POST.get('exam_id'))
        question_id = question.id

        for i in range(1, 6):
            answer_text = request.POST.get('answer-' + str(i))
            answer = QuestionAnswer.objects.create(question_id=question_id,
                                                   text=answer_text)
            answer.correct = str(i) in request.POST.getlist('correct_answers[]')
            answer.choice = request.POST.get('answer-choice-' + str(i))
            answer.save()

        return HttpResponse('aw')


class QuestionListView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    template_name = 'quiz/list.html'
    context_object_name = 'questions'

    def get_queryset(self):
        exam_id = self.kwargs.get('pk')
        return Question.objects.filter(exam__id=exam_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam_id'] = self.kwargs.get('pk')
        return context


class QuestionEditView(LoginRequiredMixin, TeacherRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if request.POST.get('change_ correct_answer'):
            answer_id = request.POST.get('id')
            answer = QuestionAnswer.objects.get(pk=answer_id)
            answer.correct = True if request.POST.get('val') == '1' else False
            answer.save()
            return HttpResponse('success')

        if request.POST.get('change_question_text'):
            question_id = request.POST.get('id')
            question_text = request.POST.get('text')

            question = Question.objects.get(id=question_id)
            question.text = question_text
            question.save()
            return HttpResponse('success')

        if request.POST.get('change_answer_text'):
            answer_id = request.POST.get('id')
            answer_text = request.POST.get('text')

            answer = QuestionAnswer.objects.get(id=answer_id)
            answer.text = answer_text
            answer.save()
            return HttpResponse('success')


class QuestionDeleteView(LoginRequiredMixin, TeacherRequiredMixin, DeleteView):
    def get_success_url(self):
        return reverse_lazy('exams:questions:list',
                            kwargs={'pk': self.kwargs.get('pk')})

    def get_object(self):
        print(self.kwargs)
        return Question.objects.get(id=self.kwargs.get('question_id'))

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
