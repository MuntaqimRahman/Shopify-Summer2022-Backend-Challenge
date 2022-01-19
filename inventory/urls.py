from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.InventoryList.as_view(), name='inventory-list'),
    path('<int:pk>/', views.InventoryDetail.as_view(), name='inventory-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)