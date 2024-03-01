from rest_framework import serializers

from ..models import Goods


class ProductSerializers(serializers.ModelSerializer):
    tag = serializers.StringRelatedField(many=True)
    category = serializers.StringRelatedField(many=True)
    detail = serializers.StringRelatedField(many=True)

    class Meta:
        model = Goods
        fields = ['id', 'category', 'tag', 'detail', 'image', 'name', 'description', 'price', 'stock',
                  'date_create', 'is_active', 'limited_edition', 'free_delivery']
