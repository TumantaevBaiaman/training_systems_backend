from django.contrib.auth.models import User
from django.db import models

from apps.products.models import Product


class Lesson(models.Model):
    products = models.ManyToManyField(Product)
    name = models.CharField(max_length=255)
    video_url = models.URLField()
    duration_seconds = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class LessonView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    viewed_duration_seconds = models.PositiveIntegerField(default=0)
    watched_datetime = models.DateTimeField(auto_now=True)

    viewed = models.BooleanField(default=False)

    def set_viewed(self, duration_watched):
        self.viewed_duration_seconds = duration_watched
        if (duration_watched / self.lesson.duration_seconds) >= 0.8:
            self.viewed = True
        else:
            self.viewed = False

    def __str__(self):
        return f"{self.lesson} math {self.user}"

    class Meta:
        verbose_name = "Просмотр"
        verbose_name_plural = "Просмотры"
