from django.contrib import admin

from orders.models import Order, Status, DetailOrder


class ProductsInline(admin.TabularInline):
    fk_name = 'order'
    model = DetailOrder


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_verbose', 'paid', 'city', 'address',
                    'order_date', 'type_delivery', 'type_payment', 'status')
    list_display_links = ('user_verbose',)
    list_filter = ('status',)
    inlines = (ProductsInline,)
    list_editable = ('status', 'paid')
    ordering = ('-order_date',)
    fieldsets = (
        (None, {
            "fields": ['city', 'address', 'paid']
        }),
        ("Delivery and Payment", {
            "fields": ["type_delivery", 'type_payment', 'status'],
            "classes": ("collapse", "wide"),
        }),
    )

    def get_queryset(self, request):
        return Order.objects.select_related('user')

    def user_verbose(self, obj: Order) -> str:
        return f"{obj.user.last_name} {obj.user.first_name}" or obj.user.email


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')
    list_display_links = ('status',)
