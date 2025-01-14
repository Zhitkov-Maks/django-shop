from typing import Tuple, Dict

from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from app_megano.models import Tags, Category, Detail, Comment, Discount


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


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display: tuple = ("id", "type", "info")
    list_display_links: tuple = ("type",)
    list_per_page: int = 100
    search_fields: tuple = ("type",)
    ordering: tuple = ("type",)
