from rest_framework import serializers
from .models import LessonView, Lesson


class LessonWithStatusSerializer(serializers.ModelSerializer):
    # Поле 'status' для информации о статусе просмотра
    status = serializers.SerializerMethodField()

    # Поле 'watched_time' для информации о времени просмотра
    watched_time = serializers.SerializerMethodField()

    def get_status(self, obj):
        # Метод для определения статуса просмотра
        return "Просмотрено" if obj['viewed'] else "Не просмотрено"

    def get_watched_time(self, obj):
        # Метод для получения времени просмотра
        return obj['viewed_duration_seconds']

    class Meta:
        model = Lesson
        fields = (
            "id",
            "status",
            "name",
            "video_url",
            "duration_seconds",
            "watched_time",
        )


class LessonViewByProductSerializer(serializers.ModelSerializer):
    # Поля для информации о уроке
    lesson_id = serializers.IntegerField(source='lesson.id')
    lesson_name = serializers.CharField(source='lesson.name')
    video_url = serializers.URLField(source='lesson.video_url')
    duration_seconds = serializers.IntegerField(source='lesson.duration_seconds')

    # Поля для информации о просмотре
    viewed = serializers.SerializerMethodField()
    viewed_duration_seconds = serializers.IntegerField()
    last_viewed_datetime = serializers.SerializerMethodField()

    def get_viewed(self, obj):
        return "Просмотрено" if obj.viewed else "Не просмотрено"

    def get_last_viewed_datetime(self, obj):
        # Преобразовать дату и время в нужный формат
        formatted_datetime = obj.watched_datetime.strftime("%Y-%m-%d %H:%M:%S")

        return formatted_datetime

    class Meta:
        model = LessonView
        fields = [
            'lesson_id', 'lesson_name', 'video_url', 'duration_seconds',
            'viewed', 'viewed_duration_seconds', 'last_viewed_datetime'
        ]