from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, db_index = True)
    text = models.TextField()
    image = models.ImageField(upload_to = 'photos', null = True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null = True)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title