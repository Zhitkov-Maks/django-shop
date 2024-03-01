from app_users.models import CustomUser
from cart.services.cart import Cart
from django.core.cache import cache
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from .forms import ReviewsForm
from .models import Goods, Category, Tags, Discount, Comment
from .services import add_category_favorite, add_queryset_top, check_product_in_cart, add_product_in_viewed_list, \
    add_product_filter, add_data_filter, get_viewed_product_week, get_sale


class HomeView(ListView):
    """Класс для отображения главной страницы"""
    model = Goods
    template_name = 'app_megano/index.html'
    context_object_name = "product_list"

    def get_queryset(self):
        """Переопределяем queryset, чтобы отфильтровать вывод товаров по сортировке топ покупок"""
        queryset = cache.get_or_set('add_queryset_top', add_queryset_top(), 10*60)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляем на главную страницу так же список с товарами с меткой ограниченная серия и
        список из 3 элементов с избранными категориями"""
        context = super().get_context_data()
        limited_list = cache.get_or_set(
            'get_limited_list', Goods.objects.prefetch_related('tag')
            .filter(limited_edition=True, is_active=True), 10*60)
        category_dict = cache.get_or_set('get_favorite_list', add_category_favorite(), 10*60)
        title = 'Интернет магазин MEGANO'
        context.update({'limited_list': limited_list, 'category_dict': category_dict, 'header': title})
        return context


class ShowCategory(ListView):
    """Класс выводит список товаров по категориям"""
    model = Category
    template_name = 'app_megano/catalog.html'
    context_object_name = "product_list"
    paginate_by = 8

    def get_queryset(self):
        category = Category.objects.get(id=self.kwargs['pk'])
        return category.categories.prefetch_related('category').prefetch_related('tag').all().order_by('-date_create')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        pk = self.kwargs['pk']
        title = f'Товары по категории {Category.objects.get(id=pk)}'
        context.update({'sortNew': True, 'header': title})
        return context


class ShowTag(ListView):
    """Класс выводит список товаров по тегам"""
    model = Tags
    template_name = 'app_megano/catalog.html'
    context_object_name = "product_list"
    paginate_by = 8

    def get_queryset(self):
        tag = Tags.objects.get(id=self.kwargs['pk'])
        return tag.tags.prefetch_related('tag').all().order_by('-date_create')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        pk = self.kwargs['pk']
        title = f'Товары по тегу {Tags.objects.get(id=pk)}'
        context.update({'sortNew': True, 'header': title})
        return context


class ProductDetailView(DetailView):
    """Класс для отображения подробной информации о товаре"""
    model = Goods
    template_name = 'app_megano/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        check = check_product_in_cart(Cart(self.request), self.object)  # Проверяем есть ли данный товар в корзине.
        count_viewed = get_viewed_product_week(self.object)  # Получаем количество просмотров за неделю
        user = self.request.user
        if self.request.user.is_authenticated:
            add_product_in_viewed_list(self.request.user, self.get_object())  # Добавляем товар в просмотренные

        form = ReviewsForm()
        product = self.get_object()
        comment = Comment.objects.select_related('user', 'user__profile').filter(goods_id=product.id)
        detail = product.detail.all()
        title = self.object

        if self.request.user.is_authenticated:
            form = ReviewsForm({
                'email': user.email,
                'name': user.first_name
            })

        context.update(
            {"product": product, 'form': form, 'check': check[0],
             'quantity': check[1], 'count_viewed': count_viewed, 'messages': comment,
             'len': len(comment), 'header': title, 'detail': detail})
        return context

    def post(self, request, pk):
        """Добавляет комментарий к товару."""
        form = ReviewsForm(request.POST)
        if self.request.user.is_authenticated:
            if form.is_valid():
                review = form.save(commit=False)
                review.goods = self.get_object()
                review.user = request.user
                form.save()
                return redirect(reverse('detail', args=[pk]))
        else:
            return redirect('login')
        return render(request, 'app_megano/product.html', context={'form': form})


class CatalogView(ListView):
    """Класс для получения товаров по выбранной категории"""
    model = Goods
    template_name = 'app_megano/catalog.html'
    context_object_name = 'product_list'
    paginate_by = 8

    def get_queryset(self):
        """Выбирает записи топ продаж за 2 месяца"""
        queryset = add_queryset_top()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        title = 'Популярные товары'
        context.update({'sortPopular': True, 'header': title})
        return context


class CatalogSortPrice(ListView):
    """Класс для сортировки товаров начиная с самых дешевых"""
    model = Goods
    template_name = 'app_megano/catalog.html'
    context_object_name = 'product_list'
    paginate_by = 8

    def get_queryset(self):
        return Goods.objects.prefetch_related('tag').all().order_by('price')

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        title = 'Сначала дешевые товары'
        context.update({'sortPriceMin': True, 'header': title})
        return context


class CatalogSortPriceMax(ListView):
    """Класс для сортировки товаров начиная с самых дорогих"""
    model = Goods
    template_name = 'app_megano/catalog.html'
    context_object_name = 'product_list'
    paginate_by = 8

    def get_queryset(self):
        return Goods.objects.prefetch_related('tag').all().order_by('-price')

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        title = 'Сначала дорогие товары'
        context.update({'sortPriceMax': True, 'header': title})
        return context


class CatalogSortReview(ListView):
    """Класс для сортировки товаров по количеству отзывов. Сначала выводятся товары где больше всего отзывов."""
    model = Goods
    template_name = 'app_megano/catalog.html'
    context_object_name = 'product_list'
    paginate_by = 8

    def get_queryset(self):
        return Goods.objects.prefetch_related('tag').all().annotate(count=Count('goods')).order_by('-count')

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        title = 'Товары с наибольшим количеством отзывов'
        context.update({'sortReview': True, 'header': title})
        return context


class CatalogSortReviewMin(ListView):
    """Класс для сортировки товаров по количеству отзывов. Сначала выводятся товары где меньше всего отзывов."""
    model = Goods
    template_name = 'app_megano/catalog.html'
    context_object_name = 'product_list'
    paginate_by = 8

    def get_queryset(self):
        return Goods.objects.prefetch_related('tag').all().annotate(count=Count('goods')).order_by('count')

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        title = 'Товары с наименьшим количеством отзывов'
        context.update({'sortReviewMin': True, 'header': title})
        return context


class CatalogSortNew(ListView):
    """Класс для вывода каталога товаров отсортированных по новизне. Сначала отображаются товары, которые были
    добавлены последними."""
    template_name = 'app_megano/catalog.html'
    context_object_name = 'product_list'
    paginate_by = 8

    def get_queryset(self):
        return Goods.objects.prefetch_related('tag').all().order_by('-date_create')

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        title = 'Сначала новые товары'
        context.update({'sortNew': True, 'header': title})
        return context


class CatalogSortOld(ListView):
    """Сначала отображаются товары, которые были добавлены первыми."""
    template_name = 'app_megano/catalog.html'
    context_object_name = 'product_list'
    paginate_by = 8

    def get_queryset(self):
        return Goods.objects.prefetch_related('tag').all().order_by('date_create')

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        title = 'Сначала старые товары'
        context.update({'sortOld': True, 'header': title})
        return context


class SearchProduct(ListView):
    """Класс для поиска товаров по вводу пользователя"""
    template_name = 'app_megano/catalog.html'
    context_object_name = 'product_list'
    paginate_by = 8

    def get_queryset(self):
        """Переопределяем queryset для поиска, сортируем по дате создания товара, поиск по названию товара"""
        query = self.request.GET.get('query').split()
        query_list = Q()
        for word in query:
            query_list &= Q(name__iregex=word)
        queryset = Goods.objects.prefetch_related('tag').filter(Q(query_list)).order_by('-date_create')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        word = self.request.GET.get('query')  # Нужно для пагинации
        title = f'Товары по тэгу {word}'
        context.update({'sortNew': True, 'header': title, 'query': word})
        return context


class SearchFilter(ListView):
    """Класс для поиска товаров по вводу пользователя"""
    template_name = 'app_megano/catalog.html'
    context_object_name = 'product_list'
    paginate_by = 8

    def get_queryset(self):
        """Переопределяем queryset для поиска"""
        queryset = add_product_filter(self.request)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        add_data_filter(self.request, context)
        context.update({'sortNew': True, 'header': 'Поиск по параметрам', 'sortFilter': True})
        return context


class ViewedProducts(ListView):
    """Класс для отображения товаров просмотренных пользователем"""
    model = CustomUser
    template_name = 'app_megano/viewed.html'
    context_object_name = 'history_list'

    def get_queryset(self):
        user = CustomUser.objects.get(id=self.kwargs['pk'])
        queryset = Goods.objects.prefetch_related('tag').filter(products__user=user)[:16]
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update({'header': 'Вы интересовались!!!'})
        return context


class Sale(ListView):
    """Класс для отображения страницы с акциями"""
    model = Discount
    template_name = 'app_megano/sale.html'
    context_object_name = 'sale_list'
    paginate_by = 16

    def get_queryset(self):
        queryset = cache.get_or_set(f'get_sale', get_sale(), 30*60)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update({'header': 'Действующие скидки'})
        return context
