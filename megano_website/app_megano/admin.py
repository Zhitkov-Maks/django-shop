from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin


from .models import Tags, Category, Detail, Goods, Comment, Gallery


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
    list_display_links = ('info',)
    list_filter = ('type',)
    ordering = ('type',)


class GalleryInline(admin.TabularInline):
    fk_name = 'goods'
    model = Gallery


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_description', 'stock', 'limited_edition')
    list_display_links = ('name',)
    list_editable = ('stock',)
    list_filter = ('category',)
    filter_horizontal = ('tag', 'detail', 'category')
    inlines = (GalleryInline,)

    def get_description(self, rec):
        if len(str(rec.description)) >= 15:
            return f'{rec.description[:15]} ...'
        else:
            return rec.description

    get_description.short_description = 'Описание'


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

