from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from .models import Product
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.db.models import Q

# Create your views here.
class TopView(TemplateView):
    template_name = "top.html"

class ProductListView(LoginRequiredMixin,ListView):
    model = Product
    paginate_by =3

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')  # 検索キーワードを取得
        if query:
            # 商品名に部分一致するものを検索 (大文字・小文字を区別しない)
            queryset = queryset.filter(Q(name__icontains=query))
        return queryset


class ProductCreateView(LoginRequiredMixin,CreateView):
    model = Product
    fields = '__all__'

class ProductUpdateView(LoginRequiredMixin,UpdateView):
     model = Product
     fields = '__all__'
     template_name_suffix = '_update_form'

class ProductDeleteView(LoginRequiredMixin,DeleteView):
     model = Product
     success_url = reverse_lazy('list')

class ProductDetailView(DetailView):
     model = Product
     context_object_name = 'product'

class LoginView(LoginView):
     form_class = AuthenticationForm
     template_name = 'login.html'
 
class LogoutView(LoginRequiredMixin, LogoutView):
     template_name = 'top.html'    

