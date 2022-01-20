from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics

from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filters
from .models import Inventory
from .serializers import InventorySerializerVersion1
from .paginations import PaginationConfig
from .filters import InventoryFilter

# Could use class based or functionally based API Views here
# Chose class based as it allows more variablity and requires less reptition in keeping with DRY

# Generics ListCreateAPIView used to take advantage of pagination and filtering without reinventing the wheel
# Chose a more manual APIView for the detailed routes as fewer features are needed and this allows new features to be added easily


# Paginate this individual view - pagination can be set globally but I wanted pagination to only affect v1 of the API
# This means if in the future we want to change the pagination settings for v2 we can do so without modifying v1's pagination
class InventoryList(generics.ListCreateAPIView):
    """
    Listing objects or creating a new one
    """

    queryset = Inventory.objects.all().order_by('pk')
    serializer_class = InventorySerializerVersion1
    pagination_class = PaginationConfig
    filterset_class = InventoryFilter
    filter_backends = (filters.backends.DjangoFilterBackend,)


class InventoryDetail(APIView):
    """
    Managing individual objects - get, update, and delete an individual object
    """

    def get_inventory(self, pk):
        try:
            return Inventory.objects.get(pk=pk)
        except Inventory.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        inventory_item = self.get_inventory(pk)
        serializer = InventorySerializerVersion1(inventory_item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        inventory_item = self.get_inventory(pk)

        serializer = InventorySerializerVersion1(
            inventory_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self,request, pk):
        inventory_item = self.get_inventory(pk)
        serializer = InventorySerializerVersion1(
            inventory_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        inventory_item = self.get_inventory(pk)
        inventory_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
