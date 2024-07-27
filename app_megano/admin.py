import csv
from csv import DictReader
from typing import Tuple, Dict, Any, List

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.safestring import mark_safe
from django_mptt_admin.admin import DjangoMpttAdmin
from io import TextIOWrapper

from orders.models import DetailOrder
from .admin_mixins import ExportAsCSVMixin
from .models import Tags, Category, Detail, Goods, Comment, Gallery, Discount
from .forms import CSVImportForms


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display: Tuple[str, str] = ("id", "name")
    list_editable: Tuple[str] = ("name",)


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields: Dict[str, Tuple[str]] = {"slug": ("name",)}
    list_display: tuple = ("id", "name", "image", "favorite")
    list_editable: tuple = ("name", "favorite")
    list_filter: tuple = ("favorite",)


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display: tuple = ("id", "type", "info")
    list_display_links: tuple = ("type",)
    list_per_page: int = 100
    search_fields: tuple = ("type",)
    ordering: tuple = ("type",)


class GalleryInline(admin.TabularInline):
    fk_name: str = "goods"
    model: Any = Gallery


class OrderInline(admin.TabularInline):
    fk_name: str = "product"
    model: Any = DetailOrder


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template: str = "app_megano/products_changelist.html"
    list_display: tuple = (
        "id",
        "name",
        "price",
        "image_show",
        "stock",
        "limited_edition",
        "is_active",
        "free_delivery",
    )

    list_display_links: tuple = ("name",)
    list_editable: tuple = (
        "stock", "limited_edition", "is_active", "free_delivery"
    )

    list_filter: tuple = ("category",)
    filter_horizontal: tuple = ("tag", "detail", "category")
    inlines: tuple = (GalleryInline, OrderInline)
    ordering: tuple = ("price",)
    fieldsets: tuple = (
        (None, {"fields": ["name", "description", "stock"]}),
        (
            "Price options",
            {
                "fields": ["price"],
                "classes": ("collapse", "wide"),
            },
        ),
        (
            "Image",
            {
                "fields": ["image"],
                "classes": ("collapse", "wide"),
            },
        ),
        (
            "Options",
            {
                "fields": ["limited_edition", "is_active", "free_delivery"],
                "classes": ("collapse", "wide"),
            },
        ),
    )
    actions: List[str] = ["export_csv"]

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForms()
            context = {
                "form": form,
            }
            return render(
                request, "admin/csv_forms.html", context
            )
        form = CSVImportForms(request.POST, request.FILES)

        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(
                request,
                "admin/csv_forms.html",
                context, status=400
            )

        csv_file = TextIOWrapper(
            form.files["csv"].file,
            encoding=request.encoding,
        )

        reader: DictReader[str] = DictReader(csv_file)
        products: List[Goods] = [Goods(**row) for row in reader]
        Goods.objects.bulk_create(products)
        self.message_user(request, "Data from csv was imported")
        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "product-csv/",
                self.import_csv,
                name="import_product_csv",
            ),
        ]
        return new_urls + urls

    def image_show(self, rec):
        """Для отображения картинок товаров в админ панели"""
        if rec.image:
            return mark_safe(
                "<img src='{}' width='60' />".format(rec.image.url)
            )
        return None

    image_show.__name__ = "Фото"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display: tuple = (
        "id", "goods", "active", "name", "email", "get_comment"
    )
    list_display_links: tuple = ("goods",)
    list_editable: tuple = ("active",)

    def get_comment(self, rec) -> str:
        if len(str(rec.comment)) >= 20:
            return f"{rec.comment[:20]} ..."
        else:
            return rec.comment

    get_comment.short_description = "Комментарий"


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display: tuple = (
        "product", "valid_from", "valid_to", "discount", "active",
    )
    list_filter: tuple = ("active", "valid_from", "valid_to")
    search_fields: tuple = ("active",)
    list_editable: tuple = ("active",)
