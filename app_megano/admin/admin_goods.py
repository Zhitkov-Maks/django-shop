from django.contrib import admin
from django.utils.safestring import mark_safe

from orders.models import DetailOrder
from app_megano.models import Goods, Gallery


class GalleryInline(admin.TabularInline):
    fk_name: str = "goods"
    model = Gallery


class OrderInline(admin.TabularInline):
    fk_name: str = "product"
    model = DetailOrder


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
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

    def image_show(self, rec):
        """Для отображения картинок товаров в админ панели"""
        if rec.image:
            return mark_safe(
                "<img src='{}' width='60' />".format(rec.image.url)
            )
        return None

    image_show.__name__ = "Фото"
