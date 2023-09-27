from django.contrib.auth.models import User
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, ProductAccess
from apps.lessons.models import LessonView
from .serializers import ProductStatsSerializer


class ProductStatsAPIView(APIView):
    def get(self, request):
        # Получить список всех продуктов
        products = Product.objects.all()

        # Инициализировать пустой список для хранения статистики по продуктам
        product_stats = []

        # Получить список всех пользователей на платформе
        all_users = User.objects.all()

        # Собрать статистику для каждого продукта
        for product in products:
            product_stat = self.get_product_stats(product, all_users)
            product_stats.append(product_stat)

        # Сериализовать статистику и вернуть в ответе API
        serialized_data = ProductStatsSerializer(product_stats, many=True)

        # Вернуть статус HTTP 200 OK и сериализованные данные
        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def get_product_stats(self, product, all_users):
        product_stat = {
            'id': product.id,
            'name': product.name,
            'owner': product.owner,
            'total_lessons_viewed': 0,
            'total_time_watched': 0,
            'total_students': 0,
            'purchase_percentage': 0,
        }

        # Получить список доступов к продукту
        accesses = ProductAccess.objects.filter(product=product)

        # Собрать статистику для каждого доступа
        for access in accesses:
            user_stats = self.get_user_stats(access.user, product)
            product_stat['total_students'] += 1
            product_stat['total_lessons_viewed'] += user_stats['total_lessons_viewed']
            product_stat['total_time_watched'] += user_stats['total_time_watched']

        # Рассчитать процент приобретения продукта
        total_users_count = all_users.count()
        if total_users_count > 0:
            purchase_percentage = (product_stat['total_students'] / total_users_count) * 100
            product_stat['purchase_percentage'] = purchase_percentage

        return product_stat

    def get_user_stats(self, user, product):
        user_stats = {
            'total_lessons_viewed': 0,
            'total_time_watched': 0,
        }

        # Получить уроки, просмотренные данным пользователем для данного продукта
        lessons_viewed = LessonView.objects.filter(user=user, lesson__products=product)

        # Собрать статистику для каждого просмотра
        for lesson in lessons_viewed:
            user_stats['total_lessons_viewed'] += 1
            user_stats['total_time_watched'] += lesson.viewed_duration_seconds

        return user_stats