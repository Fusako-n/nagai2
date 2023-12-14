from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy

from .forms import SignupForm, LoginForm, MypageEditForm
from translation.models import Translation


CustomUser = get_user_model()

class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('translation:translation')
    
    # 新規登録→ログイン済み
    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return response


class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'


class MypageView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'accounts/mypage.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['translated'] = Translation.objects.filter(user=self.request.user)
        return context


class MypageEditView(SuccessMessageMixin, UpdateView):
    form_class = MypageEditForm
    model = CustomUser
    template_name = 'accounts/mypage_edit.html'
    success_message = '内容を更新しました'
    
    def get_success_url(self):
        return reverse('users:mypage', kwargs={'pk':self.object.pk})