from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.views.generic import View
from vanilla import CreateView, TemplateView, ListView, DeleteView

from applications.quiz.models import Question, QuestionAnswer
from .forms import QuestionForm


class QuestionCreateView(CreateView):
    form_class = QuestionForm
    template_name = 'quiz/new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam_id'] = self.kwargs.get('pk')
        return context


class QuizCreateView(TemplateView):
    template_name = 'quiz/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam_id'] = self.kwargs.get('pk')
        return context

    def post(self, request, *args, **kwargs):
        question_text = request.POST.get('question')
        multiple = 2 if request.POST.get('multiple') else 1

        question = Question.objects.create(text=question_text,
                                           question_type=multiple,
                                           exam_id=request.POST.get('exam_id'))
        question_id = question.id

        for i in range(1, 6):
            answer_text = request.POST.get('answer-' + str(i))
            answer = QuestionAnswer.objects.create(question_id=question_id,
                                                   text=answer_text)
            answer.correct = str(i) in request.POST.getlist('correct_answers[]')
            answer.save()

        return HttpResponse('aw')


class QuestionListView(ListView):
    template_name = 'quiz/list.html'
    context_object_name = 'questions'

    def get_queryset(self):
        exam_id = self.kwargs.get('pk')
        return Question.objects.filter(exam__id=exam_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam_id'] = self.kwargs.get('pk')
        return context


class QuestionEditView(View):
    def post(self, request, *args, **kwargs):
        if request.POST.get('change_correct_answer'):
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


class QuestionDeleteView(DeleteView):
    def get_success_url(self):
        return reverse_lazy('exams:questions:list',
                            kwargs={'pk': self.kwargs.get('pk')})

    def get_object(self):
        print(self.kwargs)
        return Question.objects.get(id=self.kwargs.get('question_id'))

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
