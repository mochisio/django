from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from .models import Product,Category
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

        # 検索パラメータの取得
        query = self.request.GET.get('q')
        category_id = self.request.GET.get('category')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

            # デバッグのために取得した値を出力
        print(f"query: {query}, category_id: {category_id}, min_price: {min_price}, max_price: {max_price}")
        
        # 商品名での検索
        if query:
            queryset = queryset.filter(Q(name__icontains=query))

        # カテゴリでの検索
        if category_id and category_id != 'all':
            queryset = queryset.filter(category_id=category_id)

        # 価格範囲での検索
        if min_price is not None:
          try:
               min_price= int(min_price) 
               queryset = queryset.filter(price__gte=min_price)
               
          except ValueError: 
               min_price= 0
        if max_price is not None:
          try:
               max_price= int(max_price) 
               queryset = queryset.filter(price__lte=max_price)
               
          except ValueError: 
               max_price= 99999999

        
            
        
            
        
        return queryset

    # テンプレートにカテゴリ一覧を渡す
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        #価格リスト用のコンテキスト
        context['price_choices'] = [0,1000,3000,5000,10000,50000]
        return context
       

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

