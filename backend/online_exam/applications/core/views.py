from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, FormView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import LoginForm
from django.contrib.auth import login, logout, authenticate


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


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


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login/')
