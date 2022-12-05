"""Временно! Для просмотра шаблонов"""

from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request):
        category_list = [
            {'name': 'Notebook', 'price': '199'},
            {'name': 'Videocart', 'price': '299'},
            {'name': 'Smartphones', 'price': '99'}
        ]
        top_list = [
            {'name': 'Corsair Carbide Series Arctic White Steel', 'price': '85.00'},
            {'name': 'Barand New Phone Smart Business', 'price': '85.00'},
            {'name': 'Mavic PRO Mini Drones Hobby RC Quadcopter', 'price': '185'},
            {'name': 'Corsair Carbide Series Arctic White Steel', 'price': '85'},
            {'name': 'Corsair Carbide Series Arctic White Steel', 'price': '85.00'},
            {'name': 'Barand New Phone Smart Business', 'price': '85.00'},
            {'name': 'Mavic PRO Mini Drones Hobby RC Quadcopter', 'price': '185'},
            {'name': 'Corsair Carbide Series Arctic White Steel', 'price': '85'},
        ]

        limited_list = [
            {'name': 'Corsair Carbide Series Arctic White Steel', 'price': '85.00'},
            {'name': 'Barand New Phone Smart Business', 'price': '85.00'},
            {'name': 'Mavic PRO Mini Drones Hobby RC Quadcopter', 'price': '185'},
            {'name': 'Corsair Carbide Series Arctic White Steel', 'price': '85'},
            {'name': 'Corsair Carbide Series Arctic White Steel', 'price': '85.00'},
            {'name': 'Barand New Phone Smart Business', 'price': '85.00'},
            {'name': 'Mavic PRO Mini Drones Hobby RC Quadcopter', 'price': '185'},
            {'name': 'Corsair Carbide Series Arctic White Steel', 'price': '85'},
        ]

        return render(request, 'app_megano/index.html', {'category_list': category_list, 'top_list': top_list,
                                                         'limited_list': limited_list})


class DetailProduct(View):
    def get(self, request):
        return render(request, 'app_megano/product.html')


class SaleView(View):
    """Вывод списка акционных товаров."""

    def get(self, request):
        return render(request, 'app_megano/sale.html')


class CatalogView(View):
    def get(self, request):
        return render(request, 'app_megano/catalog.html')
