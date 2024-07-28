from django.contrib import admin
from django.db.models import QuerySet

from orders.models import Order, Status, DetailOrder


class ProductsInline(admin.TabularInline):
    fk_name: str = "order"
    model = DetailOrder


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display: tuple = (
        "id",
        "user_verbose",
        "paid",
        "city",
        "address",
        "order_date",
        "type_delivery",
        "type_payment",
        "status",
    )
    list_display_links: tuple = ("user_verbose",)
    list_filter: tuple = ("status",)
    inlines: tuple = (ProductsInline,)
    list_editable: tuple = ("status", "paid")
    ordering: tuple = ("-order_date",)
    fieldsets: tuple = (
        (None, {"fields": ["city", "address", "paid"]}),
        (
            "Delivery and Payment",
            {
                "fields": ["type_delivery", "type_payment", "status"],
                "classes": ("collapse", "wide"),
            },
        ),
    )

    def get_queryset(self, request) -> QuerySet:
        return Order.objects.select_related("user")

    def user_verbose(self, obj: Order) -> str:
        return f"{obj.user.last_name} {obj.user.first_name}" or obj.user.email


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display: tuple = ("id", "status")
    list_display_links: tuple = ("status",)
