from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, TemplateView

from cart.services.cart import Cart
from .forms import ReviewsForm
from .models import Goods, Category, Tags, ViewedProduct
from app_users.models import CustomUser

from .services import add_category_favorite, add_queryset_top, check_product_in_cart, add_product_in_top_list, \
    add_product_filter, add_data_filter


class HomeView(ListView):
    """Класс для отображения главной страницы"""
    model = Goods
    template_name = 'app_megano/index.html'
    context_object_name = "product_list"

    def get_queryset(self):
        """Переопределяем queryset, чтобы отфильтровать вывод товаров по сортировке топ просмотров"""
        queryset = add_queryset_top()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляем на главную страницу так же список с товарами с меткой ограниченная серия и
        список из 3 элементов с избранными категориями"""
        context = super().get_context_data()
        limited_list = Goods.objects.filter(limited_edition=True)
        category_dict = add_category_favorite()
        context.update({'limited_list': limited_list, 'category_dict': category_dict})
        return context


class ShowCategory(ListView):
    """Класс выводит список товаров по категориям"""
    model = Category
    template_name = 'app_megano/catalog.html'
    context_object_name = "product_list"

    def get_queryset(self):
        category = Category.objects.prefetch_related('categories').get(id=self.kwargs['pk'])
        return category.categories.all()


class ShowTag(ListView):
    """Класс выводит список товаров по тегам"""
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
        check = check_product_in_cart(Cart(self.request), self.object)

        if self.request.user.is_authenticated:
            add_product_in_top_list(self.request.user, self.get_object())
        form = ReviewsForm()
        context.update(
            {"product": self.get_object(), 'form': form, 'check': check[0], 'quantity': check[1]})
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


class CatalogView(ListView):
    model = Goods
    template_name = 'app_megano/catalog.html'
    context_object_name = 'product_list'
    paginate_by = 8

    def get_queryset(self):
        queryset = add_queryset_top()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        context.update({'sortPopular': True})
        return context


class CatalogSortPrice(ListView):
    """Класс для сортировки товаров начиная с самых дешевых"""
    model = Goods
    template_name = 'app_megano/catalog.html'
    context_object_name = 'product_list'
    paginate_by = 8

    def get_queryset(self):
        return Goods.objects.all().order_by('price')

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        context.update({'sortPriceMin': True})
        return context


class CatalogSortPriceMax(ListView):
    """Класс для сортировки товаров начиная с самых дорогих"""
    model = Goods
    template_name = 'app_megano/catalog.html'
    context_object_name = 'product_list'
    paginate_by = 8

    def get_queryset(self):
        return Goods.objects.all().order_by('-price')

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        context.update({'sortPriceMax': True})
        return context


class CatalogSortReview(ListView):
    """Класс для сортировки товаров по количеству отзывов. Сначала выводятся товары где больше всего отзывов.
    Обратную сортировку делать не стал, не думаю что кому-то интересны товары без отзывов."""
    model = Goods
    template_name = 'app_megano/catalog.html'
    context_object_name = 'product_list'
    paginate_by = 8

    def get_queryset(self):
        return Goods.objects.all().annotate(count=Count('goods')).order_by('-count')

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        context.update({'sortReview': True})
        return context


class CatalogSortNew(ListView):
    """Класс для вывода каталога товаров отсортированных по новизне. Сначала отображаются товары, которые были
    добавлены последними. Сортировку в обратном направлении делать не стал, так как усомнился в необходимости вывода
    товаров которые, возможно, уже не особо интересны."""
    template_name = 'app_megano/catalog.html'
    context_object_name = 'product_list'
    paginate_by = 8

    def get_queryset(self):
        return Goods.objects.all().order_by('-date_create')

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        context.update({'sortNew': True})
        return context


class SearchProduct(ListView):
    """Класс для поиска товаров по вводу пользователя"""
    template_name = 'app_megano/catalog.html'
    context_object_name = 'product_list'
    paginate_by = 16

    def get_queryset(self):
        """Переопределяем queryset для поиска"""
        query = self.request.GET.get('query').split()
        query_list = Q()
        for word in query:
            query_list |= Q(name__iregex=word)
        queryset = Goods.objects.filter(query_list)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        context.update({'search': True})
        return context


class SearchFilter(ListView):
    """Класс для поиска товаров по вводу пользователя"""
    template_name = 'app_megano/catalog.html'
    context_object_name = 'product_list'
    paginate_by = 16

    def get_queryset(self):
        """Переопределяем queryset для поиска"""
        queryset = add_product_filter(self.request)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        add_data_filter(self.request, context)
        return add_data_filter(self.request, context)


class ViewedProducts(ListView):
    """Класс для отображения товаров просмотренных пользователем"""
    model = CustomUser
    template_name = 'app_megano/viewed.html'
    context_object_name = 'history_list'

    def get_queryset(self):
        user = CustomUser.objects.get(id=self.kwargs['pk'])
        return user.persons.all().order_by('-viewed_date')[:16]
