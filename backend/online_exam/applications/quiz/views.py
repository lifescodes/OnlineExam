from django.http import HttpResponse
from vanilla import CreateView, TemplateView

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
            answer_text = request.POST.get('answer-'+str(i))
            answer = QuestionAnswer.objects.create(question_id=question_id,
                                                   text=answer_text)
            answer.correct = str(i) in request.POST.getlist('correct_answers[]')
            answer.save()

        return HttpResponse('aw')
