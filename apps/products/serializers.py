from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductStatsSerializer(serializers.ModelSerializer):
    # Поля для информации о продукте
    product_id = serializers.IntegerField(source='id')
    product_name = serializers.CharField(source='name')
    product_owner = serializers.PrimaryKeyRelatedField(source='owner', queryset=User.objects.all())

    # Поля для статистики
    total_lessons_viewed = serializers.IntegerField()
    total_time_watched = serializers.IntegerField()
    total_students = serializers.IntegerField()
    purchase_percentage = serializers.FloatField()

    class Meta:
        model = Product
        fields = (
            'product_id', 'product_name', 'product_owner',
            'total_lessons_viewed', 'total_time_watched', 'total_students', 'purchase_percentage'
        )