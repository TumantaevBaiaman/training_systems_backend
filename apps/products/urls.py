from django.urls import path
from .views import ProductStatsAPIView

urlpatterns = [
    path('stats/', ProductStatsAPIView.as_view(), name='product-stats'),
]