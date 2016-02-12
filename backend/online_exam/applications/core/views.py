import datetime
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import View, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from vanilla.views import FormView

from applications.exam.models import Exam
from applications.user.models import User, Profile
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exams = self.get_exams()
        context['exams'] = exams
        return context

    def get_exams(self):
        user = self.request.user
        if user.is_teacher():
            return Exam.objects.filter(user=user)
        return Exam.objects.all()


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


class RegisterView(TemplateView):
    template_name = 'register.html'

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        day = request.POST.get('day')
        month = request.POST.get('month')
        year = request.POST.get('year')

        gender = request.POST.get('gender')
        username = request.POST.get('username')
        passwd = request.POST.get('passwd')
        print(passwd)

        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')

        try:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username
            )
            user.set_password(passwd)
            user.save()

            birth_date = datetime.date(int(year), int(month), int(day))

            Profile.objects.create(
                user=user,
                gender=gender,
                address=address,
                city=city,
                zip_code=zip_code,
                phone=phone,
                birthday=birth_date
            )

            return HttpResponseRedirect(reverse_lazy('core:login'))

        except:
            return self.get(request)
