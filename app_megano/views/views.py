from django.http import HttpResponse

from app_users.models import CustomUser
from cart.services.cart import Cart
from django.core.cache import cache
from django.db.models import Count, Q, QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from app_megano.forms import ReviewsForm
from app_megano.models import Goods, Category, Tags, Discount, Comment
from app_megano.crud import (
    add_category_favorite,
    add_queryset_top,
    add_product_in_viewed_list,
    add_product_filter,
    get_viewed_product_period,
    get_sale, search_product_queryset,
)
from app_megano.services import check_product_in_cart, add_data_filter


class HomeView(ListView):
    """Класс для отображения главной страницы"""

    model = Goods
    template_name: str = "app_megano/index.html"
    context_object_name: str = "product_list"

    def get_queryset(self) -> QuerySet:
        """
        Переопределяем queryset, чтобы отфильтровать вывод товаров по
        сортировке топ покупок.
        """
        return cache.get_or_set(
            "add_queryset_top", add_queryset_top(), 10 * 60
        )

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        Добавляем на главную страницу так же список с товарами с меткой
        ограниченная серия и список из 3 элементов с избранными категориями.
        """
        context: dict = super().get_context_data()

        limited_list: QuerySet = cache.get_or_set(
            "get_limited_list",
            Goods.objects.prefetch_related("tag").filter(
                limited_edition=True, is_active=True
            ),
            10 * 60,
        )

        category_dict: QuerySet = cache.get_or_set(
            "get_favorite_list", add_category_favorite(), 10 * 60
        )

        context.update(
            {
                "limited_list": limited_list,
                "category_dict": category_dict,
                "header": "Интернет магазин MEGANO",
            }
        )
        return context


class ShowCategory(ListView):
    """Класс выводит список товаров по категориям."""

    model = Category
    template_name: str = "app_megano/catalog.html"
    context_object_name: str = "product_list"
    paginate_by: int = 8

    def get_queryset(self) -> QuerySet:
        """
        Переопределяем метод, чтобы прикрепить к категориям еще и теги, для
        отображения на странице.
        """
        category: Category = Category.objects.get(id=self.kwargs["pk"])
        return (
            category.categories.prefetch_related("category")
            .prefetch_related("tag")
            .all()
            .order_by("-date_create")
        )

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        Переопределяем метод, для того чтобы прикрепить тип сортировки
        и header.
        """
        context: dict = super().get_context_data()
        pk: int = self.kwargs["pk"]
        context.update(
            {
                "sortNew": True,
                "header": f"Товары по категории {Category.objects.get(id=pk)}"}
        )
        return context


class ShowTag(ListView):
    """Класс выводит список товаров по тегам."""

    model = Tags
    template_name: str = "app_megano/catalog.html"
    context_object_name: str = "product_list"
    paginate_by: int = 8

    def get_queryset(self) -> QuerySet:
        """
        Переопределяем метод, чтобы подгрузить все, что нужно за один раз.
        """
        tag: Tags = Tags.objects.get(id=self.kwargs["pk"])
        return tag.tags.prefetch_related("tag").all().order_by("-date_create")

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        Переопределяем метод, для того чтобы прикрепить тип сортировки
        и header.
        """
        context: dict = super().get_context_data()
        pk: int = self.kwargs["pk"]
        context.update(
            {
                "sortNew": True,
                "header": f"Товары по тегу {Tags.objects.get(id=pk)}"}
        )
        return context


class ProductDetailView(DetailView):
    """Класс для отображения подробной информации о товаре"""

    model = Goods
    template_name: str = "app_megano/product.html"

    def get_context_data(self, **kwargs) -> dict:
        """
        Переопределяем метод, чтобы прикрепить все, что нам нужно, для
        полноценной работы.
        """
        context: dict = super().get_context_data()

        # Проверяем есть ли данный товар в корзине.
        check: tuple = check_product_in_cart(Cart(self.request), self.object)

        # Получаем количество просмотров за неделю
        count_viewed: int = get_viewed_product_period(self.object)

        user: CustomUser = self.request.user
        # Добавляем товар в просмотренные
        if self.request.user.is_authenticated:
            add_product_in_viewed_list(user, self.get_object())

        form = ReviewsForm()
        product: Goods = self.get_object()
        comment: QuerySet = (
            Comment.objects
            .select_related('user', 'user__profile')
            .filter(goods_id=product.id)
        )
        detail = product.detail.prefetch_related("details").all()

        if self.request.user.is_authenticated:
            form = ReviewsForm({
                'email': user.email,
                'name': user.first_name
            })

        context.update(
            {
                "product": product,
                'form': form,
                'check': check[0],
                'quantity': check[1],
                'count_viewed': count_viewed,
                'messages': comment,
                'len': len(comment),
                'header': self.object,
                'detail': detail
            }
        )
        return context

    def post(self, request, pk) -> HttpResponse:
        """Добавляет комментарий к товару."""
        form = ReviewsForm(request.POST)

        if self.request.user.is_authenticated:
            if form.is_valid():
                review: Comment = form.save(commit=False)
                review.goods = self.get_object()
                review.user = request.user
                form.save()
                return redirect(reverse("detail", args=[pk]))

        else:
            return redirect("login")

        return render(
            request,
            "app_megano/product.html",
            context={"form": form}
        )


class CatalogView(ListView):
    """Класс для получения товаров по выбранной категории"""

    model = Goods
    template_name = "app_megano/catalog.html"
    context_object_name = "product_list"
    paginate_by = 8

    def get_queryset(self):
        """Выбирает записи топ продаж за 2 месяца"""
        queryset = add_queryset_top()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        title = "Популярные товары"
        context.update({"sortPopular": True, "header": title})
        return context


class CatalogSortPrice(ListView):
    """Класс для сортировки товаров начиная с самых дешевых"""

    model = Goods
    template_name = "app_megano/catalog.html"
    context_object_name = "product_list"
    paginate_by = 8

    def get_queryset(self):
        return Goods.objects.prefetch_related("tag").all().order_by("price")

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        title = "Сначала дешевые товары"
        context.update({"sortPriceMin": True, "header": title})
        return context


class CatalogSortPriceMax(ListView):
    """Класс для сортировки товаров начиная с самых дорогих"""

    model = Goods
    template_name = "app_megano/catalog.html"
    context_object_name = "product_list"
    paginate_by = 8

    def get_queryset(self):
        return Goods.objects.prefetch_related("tag").all().order_by("-price")

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        title = "Сначала дорогие товары"
        context.update({"sortPriceMax": True, "header": title})
        return context


class CatalogSortReview(ListView):
    """Класс для сортировки товаров по количеству отзывов. Сначала выводятся товары где больше всего отзывов."""

    model = Goods
    template_name = "app_megano/catalog.html"
    context_object_name = "product_list"
    paginate_by = 8

    def get_queryset(self):
        return (
            Goods.objects.prefetch_related("tag")
            .all()
            .annotate(count=Count("goods"))
            .order_by("-count")
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        title = "Товары с наибольшим количеством отзывов"
        context.update({"sortReview": True, "header": title})
        return context


class CatalogSortReviewMin(ListView):
    """
    Класс для сортировки товаров по количеству отзывов. Сначала выводятся
    товары где меньше всего отзывов.
    """

    model = Goods
    template_name: str = "app_megano/catalog.html"
    context_object_name: str = "product_list"
    paginate_by: int = 8

    def get_queryset(self) -> QuerySet:
        """Переопределили, чтобы добавить сортировку и избежать
        лишних обращений к бд.
        """
        return (
            Goods.objects.prefetch_related("tag")
            .all()
            .annotate(count=Count("goods"))
            .order_by("count")
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне."""
        context = super().get_context_data()
        context.update(
            {
                "sortReviewMin": True,
                "header": "Товары с наименьшим количеством отзывов"
            }
        )
        return context


class CatalogSortNew(ListView):
    """
    Класс для вывода каталога товаров отсортированных по новизне.
    Сначала отображаются товары, которые были добавлены последними.
    """

    template_name: str = "app_megano/catalog.html"
    context_object_name: str = "product_list"
    paginate_by: int = 8

    def get_queryset(self) -> QuerySet:
        """Переопределил, чтобы избежать лишних запросов к бд."""
        return Goods.objects.prefetch_related("tag").all().order_by(
            "-date_create"
        )

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """Добавляет идентификатор для отображения сортировки в шаблоне."""
        context: dict = super().get_context_data()
        context.update(
            {"sortNew": True, "header": "Сначала новые товары"}
        )
        return context


class CatalogSortOld(ListView):
    """Сначала отображаются товары, которые были добавлены первыми."""

    template_name: str = "app_megano/catalog.html"
    context_object_name: str = "product_list"
    paginate_by: str = 8

    def get_queryset(self) -> QuerySet:
        """Переопределил, чтобы избежать лишних запросов к бд."""
        return Goods.objects.prefetch_related("tag").all().order_by(
            "date_create"
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        context.update(
            {"sortOld": True, "header": "Сначала старые товары"}
        )
        return context


class SearchProduct(ListView):
    """Класс для поиска товаров по вводу пользователя"""

    template_name: str = "app_megano/catalog.html"
    context_object_name: str = "product_list"
    paginate_by: int = 8

    def get_queryset(self) -> QuerySet:
        """
        Переопределяем queryset для поиска, сортируем по дате создания
        товара, поиск по названию товара.
        """
        return search_product_queryset(self.request.GET.get("query").split())

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """Добавляет идентификатор для отображения сортировки в шаблоне."""
        context: dict = super().get_context_data()
        context.update(
            {
                "sortNew": True,
                "header": f"Товары по тэгу {self.request.GET.get('query')}",
                "query": self.request.GET.get("query")}
        )
        return context


class SearchFilter(ListView):
    """Класс для поиска товаров по вводу пользователя"""

    template_name: str = "app_megano/catalog.html"
    context_object_name: str = "product_list"
    paginate_by: int = 8

    def get_queryset(self) -> QuerySet:
        """Переопределяем queryset для поиска"""
        return add_product_filter(self.request)

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """Добавляет идентификатор для отображения сортировки в шаблоне."""
        context: dict = super().get_context_data()
        add_data_filter(self.request, context)
        context.update(
            {
                "sortNew": True,
                "header": "Поиск по параметрам",
                "sortFilter": True
            }
        )
        return context


class ViewedProducts(ListView):
    """Класс для отображения товаров просмотренных пользователем"""

    model = CustomUser
    template_name: str = "app_megano/viewed.html"
    context_object_name: str = "history_list"

    def get_queryset(self):
        """Переопределил, чтобы не выполнялось лишних запросов к бд."""
        user = CustomUser.objects.get(id=self.kwargs["pk"])
        return Goods.objects.prefetch_related("tag").filter(
            products__user=user
        )[:16]

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """Нужен только, чтобы добавить header в контекст."""
        context: dict = super().get_context_data()
        context.update({"header": "Вы интересовались!!!"})
        return context


class Sale(ListView):
    """Класс для отображения страницы с акциями"""

    model = Discount
    template_name: str = "app_megano/sale.html"
    context_object_name: str = "sale_list"
    paginate_by: int = 16

    def get_queryset(self) -> QuerySet:
        """
        Переопределяем, чтобы кешировать ответ, так как скидки обновляются
        не так часто.
        """
        return cache.get_or_set("get_sale", get_sale(), 30 * 60)

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """Нужен только, чтобы добавить header в контекст."""
        context: dict = super().get_context_data()
        context.update({"header": "Действующие скидки"})
        return context
