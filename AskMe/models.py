from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by('-created_date')

    def best_questions(self):
        return self.ordered_by('-rate')

    def hot_questions(self):
        return self.new_questions().order_by('-rate')


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Profile(models.Model):
    id = models.IntegerField(default=0,primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(default="email")
    # name = models.CharField(max_length=30)
    # password = models.CharField(max_length=30)
    photo = models.ImageField(default='images/cool_programmer.jpg')
    # created_date = models.DateTimeField(default=timezone.now)
    rate = models.IntegerField(default=0)

    #
    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    text = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.text


class Answer(models.Model):
    id = models.IntegerField(default=-1, primary_key=True)
    title = models.TextField(default="")
    content = models.TextField(default="")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    isRight = models.BooleanField(default=False)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return self.content


class Question(models.Model):
    id = models.IntegerField(default=-1, primary_key=True)
    title = models.TextField(default="")
    content = models.TextField(default="")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag)
    answers = models.ManyToManyField(Answer)
    rate = models.IntegerField(default=0)
    list = QuestionManager()

    def __str__(self):
        return self.title
