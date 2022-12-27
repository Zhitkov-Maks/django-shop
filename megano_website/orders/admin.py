from django.contrib import admin

from orders.models import Order, Status


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'city', 'address', 'order_date', 'type_delivery', 'type_payment', 'status')
    list_display_links = ('user',)
    ordering = ('-order_date',)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'comment')
    list_display_links = ('status',)
