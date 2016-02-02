from django.http import HttpResponse
from vanilla import CreateView, TemplateView

from applications.quiz.models import Question
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
        return HttpResponse('aw')
        # return self.get(request)
