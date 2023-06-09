from django.contrib import admin
from django.utils.safestring import mark_safe
from django_mptt_admin.admin import DjangoMpttAdmin

from .admin_mixins import ExportAsCSVMixin
from .models import Tags, Category, Detail, Goods, Comment, Gallery, Discount


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


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    list_display = ('id', 'name', 'price', 'image_show', 'stock', 'limited_edition', 'is_active', 'free_delivery')
    list_display_links = ('name',)
    list_editable = ('stock', 'limited_edition', 'is_active', 'free_delivery')
    list_filter = ('category',)
    filter_horizontal = ('tag', 'detail', 'category')
    inlines = (GalleryInline,)
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
