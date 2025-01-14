from django.contrib.auth.models import User
from django.http import HttpResponse

from app_megano.models.model_comments import Comment
from app_megano.models.model_discount import Discount
from app_megano.models.model_goods import Goods
from app_megano.models.model_tags_categories import Category, Tags
from app_megano.services import collection_data
from app_users.models import CustomUser
from django.core.cache import cache
from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from app_megano.forms import ReviewsForm
from app_megano.crud import (
    add_category_favorite,
    add_queryset_top,
    get_sale
)


class HomeView(ListView):
    """Класс для отображения главной страницы сайта."""

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
                "category_dict": category_dict
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


class ProductDetailView(DetailView):
    """Класс для отображения подробной информации о товаре."""

    model = Goods
    template_name: str = "app_megano/product.html"

    def get_context_data(self, **kwargs) -> dict:
        """
        Переопределяем метод, чтобы прикрепить все, что нам нужно, для
        полноценной работы.
        """
        context: dict = super().get_context_data()
        collection_data(self, context)
        form = ReviewsForm()
        user: User = self.request.user
        if self.request.user.is_authenticated:
            form = ReviewsForm({
                'email': user.email,
                'name': user.first_name
            })

        context.update({'form': form})
        return context

    def post(self, request, pk) -> HttpResponse:
        """
        Добавляет комментарий к товару. Комментировать могут только
        зарегистрированные пользователи.
        """
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
