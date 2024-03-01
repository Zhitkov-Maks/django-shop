from rest_framework import serializers


from ..models import Order


class OrderSerializers(serializers.ModelSerializer):
    status = serializers.StringRelatedField(many=False)
    orders = serializers.StringRelatedField(many=True)

    class Meta:
        model = Order
        fields = ['id', 'full_name', 'phone', 'email', 'city', 'address', 'status',
                  'type_delivery', 'type_payment', 'order_date', 'total_price', 'paid', 'comment', 'orders']
