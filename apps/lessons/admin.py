from django.contrib import admin

from .models import Lesson, LessonView


@admin.register(Lesson)
class PLessonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "duration_seconds",
    )


@admin.register(LessonView)
class LessonViewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "lesson",
        "viewed_duration_seconds",
        "viewed",
    )
