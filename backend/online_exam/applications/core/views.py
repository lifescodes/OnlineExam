from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from vanilla.views import FormView, TemplateView
from .forms import LoginForm


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TeacherRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)\
            if request.user.is_teacher() else HttpResponseRedirect('/')


class StudentRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)\
            if request.user.is_student() else HttpResponseRedirect('/')


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse('core:login'))

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('core:home'))
        return super().get(request, *args, **kwargs)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login/')


class RegisterView(FormView):
    template_name = 'register.html'
    success_url = reverse_lazy('login')
