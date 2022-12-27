from rest_framework import serializers

from .models import SiteSettings


class SiteSettingsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SiteSettings
        fields = ['logotype', 'phone', 'email', 'skype', 'address', 'price_delivery_express', 'price', 'min_sum']
