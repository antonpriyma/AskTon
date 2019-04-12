from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Profile(models.Model):
    email = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    photo = models.ImageField
    created_date = models.DateTimeField(default=timezone.now)
    rate = models.IntegerField(default=0)
    user = models.OneToOneField(User)

class Tag(models.Model):
    text = models.CharField(max_length=64)

    def __str__(self):
        return self.text



class Answer(models.Model):
    id = models.IntegerField
    title = models.TextField
    content = models.TextField
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    isRight = models.BooleanField
    rate = models.IntegerField

class Question(models.Model):
    id = models.IntegerField
    title = models.TextField
    content = models.TextField
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag)
    answers = models.ManyToManyField(Answer)
    rate = models.IntegerField

class Profile()






