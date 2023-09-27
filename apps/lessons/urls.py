from django.urls import path
from .views import LessonListProductsAPIView, LessonViewByProduct

urlpatterns = [
    path('list/<int:user_id>/', LessonListProductsAPIView.as_view(), name='lesson-access-list'),
    path('list/<int:user_id>/<int:product_id>/', LessonViewByProduct.as_view(), name='lesson-access-by-product')
]