from cgitb import lookup
from django_filters import rest_framework as filters
from .models import Inventory

from taggit.forms import TagField

class TagFilter(filters.CharFilter):
    field_class = TagField

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('lookup_expr', 'in')
        super().__init__(*args, **kwargs)


class InventoryFilter(filters.FilterSet):
    min_msrp = filters.NumberFilter(field_name="msrp", lookup_expr="gte")
    max_msrp = filters.NumberFilter(field_name="msrp", lookup_expr="lte")

    min_amount = filters.NumberFilter(field_name="amount", lookup_expr="gte")
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr="lte")

    # Made the filters for name and description case insensitive
    name = filters.CharFilter(field_name="name",lookup_expr='icontains')
    description = filters.CharFilter(field_name="description",lookup_expr='icontains')
    tags = TagFilter(field_name='tags__name')

    class Meta:
        model = Inventory
        fields=['msrp','amount','name','description','tags']


