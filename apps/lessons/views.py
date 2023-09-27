from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LessonView, Lesson
from .serializers import LessonWithStatusSerializer, LessonViewByProductSerializer


class LessonListProductsAPIView(APIView):
    def get(self, request, user_id):
        # Получить уроки, к которым у пользователя есть доступ
        accessible_lessons = self.get_accessible_lessons(user_id)

        # Получить уроки с информацией о статусе и времени просмотра
        lessons_with_status = self.get_lessons_with_status(user_id, accessible_lessons)

        # Вернуть результат в формате JSON
        return Response(lessons_with_status, status=status.HTTP_200_OK)

    def get_accessible_lessons(self, user_id):
        # Получить уроки, к которым у пользователя есть доступ
        return Lesson.objects.filter(products__productaccess__user_id=user_id)

    def get_lessons_with_status(self, user_id, accessible_lessons):
        lessons_with_status = []

        # Для каждого урока, получить информацию о статусе и времени просмотра
        for lesson in accessible_lessons:
            lesson_view = self.get_lesson_view(user_id, lesson)
            lesson_data = self.serialize_lesson_with_status(lesson, lesson_view)
            lessons_with_status.append(lesson_data)

        return lessons_with_status

    def get_lesson_view(self, user_id, lesson):
        try:
            # Получить информацию о просмотре урока для пользователя
            return LessonView.objects.get(user_id=user_id, lesson=lesson)
        except LessonView.DoesNotExist:
            # Если информации о просмотре нет, вернуть None
            return None

    def serialize_lesson_with_status(self, lesson, lesson_view):
        lesson_data = {
            'id': lesson.id,
            'name': lesson.name,
            'video_url': lesson.video_url,
            'duration_seconds': lesson.duration_seconds,
            'viewed': False,
            'viewed_duration_seconds': 0
        }

        # Если есть информация о просмотре, обновить данные
        if lesson_view:
            lesson_data['viewed'] = lesson_view.viewed
            lesson_data['viewed_duration_seconds'] = lesson_view.viewed_duration_seconds

        # Сериализовать данные урока с информацией о статусе и времени просмотра
        return LessonWithStatusSerializer(lesson_data).data


class LessonViewByProduct(APIView):
    def get(self, request, user_id, product_id):
        # Получить уроки, связанные с указанным продуктом, к которым у пользователя есть доступ
        accessible_lessons = self.get_accessible_lessons(user_id, product_id)

        # Получить информацию о просмотре уроков для пользователя и продукта
        lesson_accesses = LessonView.objects.filter(user_id=user_id, lesson__in=accessible_lessons)

        # Сериализовать данные с информацией о статусе, времени просмотра и дате последнего просмотра
        serialized_data = LessonViewByProductSerializer(lesson_accesses, many=True).data

        return Response(serialized_data, status=status.HTTP_200_OK)

    def get_accessible_lessons(self, user_id, product_id):
        # Получить уроки, связанные с указанным продуктом, к которым у пользователя есть доступ
        return Lesson.objects.filter(products__productaccess__user_id=user_id, products__id=product_id)
