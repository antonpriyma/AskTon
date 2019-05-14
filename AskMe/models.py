from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by('-created_date')

    def best_questions(self):
        return self.order_by('-rate')

    def hot_questions(self):
        return self.new_questions().order_by('-rate')


class Profile(AbstractUser):
    photo = models.ImageField(default='images/cool_programmer.jpg')
    rate = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class Vote(models.Model):
    # unique_together=(
    #     'object_id',
    #     'type_vote',
    #     'content_object',
    #     'user'
    # )
    LIKE = 1
    DISLIKE = 0

    VOTES = (
        (DISLIKE, 'Dislike'),
        (LIKE, 'Like')
    )

    type_vote = models.SmallIntegerField(verbose_name="Vote", choices=VOTES)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    # objects = LikeDislikeManager()


class Tag(models.Model):
    text = models.CharField(max_length=64, unique=True)


    def __str__(self):
        return self.text


class Post(models.Model):
    Vote = GenericRelation(Vote)
    title = models.CharField(max_length=20, default="")
    content = models.TextField(default="")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    rate = models.IntegerField(default=0)

    class Meta:
        abstract = True



class Question(Post):
    tags = models.ManyToManyField(Tag)

    list = QuestionManager()

    # TODO: Доделать голосование

    def __str__(self):
        return self.title


class Answer(Post):
    isRight = models.BooleanField(default=False)
    questions = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.content

