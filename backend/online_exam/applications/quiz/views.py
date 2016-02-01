from vanilla import CreateView, TemplateView
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
        print(request.POST)
