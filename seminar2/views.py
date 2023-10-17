from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import Event
from .forms import SearchForm, SignUpForm


class LoginView(TemplateView):
    template_name = 'registration/login.html'


class SignupView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class IndexView(ListView):
    template_name = 'seminar2/index.html'
    model = Event
    
    def get_queryset(self):
        queryset = Event.objects.order_by('date')
        form = SearchForm(self.request.GET)
        if form.is_valid():
            # キーワード検索
            keyword = form.cleaned_data.get('keyword')
            if keyword:
                queryset = queryset.filter(Q(name__icontains=keyword)|Q(description__icontains=keyword))
            # エリア検索
            area = form.cleaned_data.get('area')
            if area:
                queryset = queryset.filter(area=area)
            # カテゴリー検索
            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)
            # 日付検索
            date = form.cleaned_data.get('date')
            if date:
                queryset = queryset.filter(date=date)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = SearchForm(self.request.GET)
        context['form'] = form
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'seminar2/event_detail.html'