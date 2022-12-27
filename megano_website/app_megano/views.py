from django.contrib.auth.models import User
from django.db.models import Min, Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView

from cart.services.cart import Cart
from .forms import ReviewsForm
from .models import Goods, Category, Tags, ViewedProduct


class HomeView(ListView):
    """Главная страница."""
    model = ViewedProduct
    template_name = 'app_megano/index.html'
    context_object_name = "product_list"

    def get_queryset(self):
        current_datetime = timezone.now()
        queryset = ViewedProduct.objects.values('goods')\
            .distinct()\
            .annotate(sum=Sum("quantity")) \
            .filter(viewed_date__year=current_datetime.year,
                    viewed_date__month=current_datetime.month).order_by("-sum")
        product_list = []
        for product in queryset:
            product_list.append(Goods.objects.get(id=product['goods']))
        return product_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        limited_list = Goods.objects.filter(limited_edition=True)
        category_list = Category.objects.filter(favorite=True)
        category_dict = {}
        for cat in category_list[:3]:
            category_dict[cat.id] = [cat, cat.categories.aggregate(Min('price'))]
        context.update({'limited_list': limited_list, 'category_list': category_dict})
        return context


class AddProduct(View):
    def get(self, request, pk):
        cart = Cart(request)

        product = get_object_or_404(Goods, id=pk)
        cart.add(
            product=product,
            quantity=1
        )
        return render(request, 'app_megano/buy.html', {'object': product})


class ShowCategory(ListView):
    """Класс выводит список товаров по категориям"""
    model = Category
    template_name = 'app_megano/catalog.html'
    context_object_name = "product_list"

    def get_queryset(self):
        category = Category.objects.prefetch_related('categories').get(id=self.kwargs['pk'])
        return category.categories.all()


class ShowTag(ListView):
    """Класс выводит список товаров по категориям"""
    model = Tags
    template_name = 'app_megano/catalog.html'
    context_object_name = "product_list"

    def get_queryset(self):
        tag = Tags.objects.get(id=self.kwargs['pk'])
        return tag.tags.all()


class ProductDetailView(DetailView):
    """Класс для отображения подробной информации о товаре"""
    model = Goods
    template_name = 'app_megano/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            user = self.request.user
            product = self.get_object()
            if ViewedProduct.objects.filter(user_id=user.id, goods_id=product.id).exists():
                viewed_product = ViewedProduct.objects.get(user_id=user.id, goods_id=product.id)
                viewed_product.viewed_date = timezone.now()
                viewed_product.save()
            else:
                ViewedProduct.objects.create(user=user, goods=product, viewed_date=timezone.now())
        form = ReviewsForm()
        context.update({"product": self.get_object(), 'form': form})
        return context

    def post(self, request, pk):
        form = ReviewsForm(request.POST)
        if self.request.user.is_authenticated:
            if form.is_valid():
                review = form.save(commit=False)
                review.goods = self.get_object()
                form.save()
                return redirect(reverse('detail', args=[pk]))
        else:
            return redirect('login')
        return render(request, 'app_megano/product.html', context={'form': form})


class SaleView(View):
    """Вывод списка акционных товаров."""

    def get(self, request):
        cart = Cart(self.request)
        return render(request, 'app_megano/sale.html', {'cart': cart})


class CatalogView(ListView):
    template_name = 'app_megano/catalog.html'
    model = Goods
    context_object_name = 'product_list'
    paginate_by = 8

    def get_queryset(self):
        return Goods.objects.all().order_by('-date_create')


class ViewedProducts(ListView):
    model = User
    template_name = 'app_megano/viewed.html'
    context_object_name = 'history_list'

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs['pk'])
        return user.persons.all().order_by('-viewed_date')[:50]
