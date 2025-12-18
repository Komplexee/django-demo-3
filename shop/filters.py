from django_filters import rest_framework as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    category__name = filters.CharFilter(lookup_expr='icontains')
    manufacturer__name = filters.CharFilter(lookup_expr='icontains')
    supplier__name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name', 'description', 'category__name', 'manufacturer__name', 'supplier__name']
