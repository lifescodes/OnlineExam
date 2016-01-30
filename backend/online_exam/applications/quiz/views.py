from vanilla import CreateView
from .forms import QuestionForm


class QuestionCreateView(CreateView):
    form_class = QuestionForm
    template_name = 'quiz/new.html'
