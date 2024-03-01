from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from .models import SiteSettings
from .serializers import SiteSettingsSerializer


class SettingsAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer

    def get(self, request):
        return self.list(request)
