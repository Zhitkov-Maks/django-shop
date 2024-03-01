from csv import DictReader

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
    list_display = ('id', 'name')
    list_editable = ('name',)


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {"slug": ('name',)}
    list_display = ('id', 'name', 'image', 'favorite')
    list_editable = ('name', 'favorite')
    list_filter = ('favorite',)


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'info')
    list_display_links = ('type',)
    list_per_page = 100
    search_fields = ('type',)
    ordering = ('type',)


class GalleryInline(admin.TabularInline):
    fk_name = 'goods'
    model = Gallery


class OrderInline(admin.TabularInline):
    fk_name = 'product'
    model = DetailOrder


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template = "app_megano/products_changelist.html"
    list_display = ('id', 'name', 'price', 'image_show', 'stock', 'limited_edition', 'is_active', 'free_delivery')
    list_display_links = ('name',)
    list_editable = ('stock', 'limited_edition', 'is_active', 'free_delivery')
    list_filter = ('category',)
    filter_horizontal = ('tag', 'detail', 'category')
    inlines = (GalleryInline, OrderInline)
    ordering = "price",
    fieldsets = (
        (None, {
            "fields": ['name', 'description', 'stock']
        }),
        ("Price options", {
            "fields": ["price"],
            "classes": ("collapse", "wide"),
        }),
        ("Image", {
            "fields": ["image"],
            "classes": ("collapse", "wide"),
        }),
        ("Options", {
            "fields": ['limited_edition', 'is_active', 'free_delivery'],
            "classes": ("collapse", "wide"),
        })
    )
    actions = ["export_csv"]

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForms()
            context = {
                "form": form,
            }
            return render(request, "admin/csv_forms.html", context)
        form = CSVImportForms(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/csv_forms.html", context, status=400)
        csv_file = TextIOWrapper(
            form.files["csv"].file,
            encoding=request.encoding,
        )
        reader = DictReader(csv_file)
        products = [Goods(**row) for row in reader]
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
            return mark_safe("<img src='{}' width='60' />".format(rec.image.url))
        return None

    image_show.__name__ = "Фото"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'goods', 'active', 'name', 'email', 'get_comment')
    list_display_links = ('goods',)
    list_editable = ('active',)

    def get_comment(self, rec):
        if len(str(rec.comment)) >= 20:
            return f'{rec.comment[:20]} ...'
        else:
            return rec.comment

    get_comment.short_description = 'Комментарий'


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['product', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['active']
    list_editable = ['active']
