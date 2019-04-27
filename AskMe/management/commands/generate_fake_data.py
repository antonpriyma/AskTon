import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.db.models import Max, Min

from AskMe.models import Question
from AskMe.models import Tag
from AskMe.models import Profile
from AskMe.models import Vote
from AskMe.models import Answer
from django.contrib.auth.models import User
from faker import Faker


def get_random_element(qs, min_pk, max_pk):
    if max_pk is None:
        max_pk = qs.aggregate(Max('pk'))
    if min_pk is None:
        min_pk = qs.aggregate(Min('pk'))
    while True:
        print("min_pk = ",min_pk ,max_pk)
        try_pk = random.randint(min_pk['pk__min'], max_pk['pk__max'])
        try:
            found = qs.get(pk=try_pk)
            return found
        except qs.model.DoesNotExist:
            pass


def get_borders(qs):
    return qs.aggregate(Min('pk'))['pk__min'], qs.aggregate(Max('pk'))['pk__max']


class Command(BaseCommand):

    fake = Faker()

    def handle(self, *args, **options):

        for i in range(options['user_count']):
            cur_user = Profile(username=self.fake.last_name() + 'XxX' + str(i),
                            password=self.fake.date(pattern="%d.%m.%Y", end_datetime=None))

            try:
                cur_user.save()

                self.stdout.write('Info: Profile Saved ' + cur_user.username)
            except IntegrityError:
                self.stdout.write('Info: Profile DUPLICATION. Repeating #' + str(i))

                cur_user.username += 'XxX' + str(i)
                cur_user.save()

        min_profile_pk, max_profile_pk = get_borders(Profile.objects.all())
        self.stdout.write(self.style.SUCCESS('Successfully generate %d users' % options['user_count']))

        for i in range(options['tags_count']):
            tag = Tag(text=self.fake.word(ext_word_list=None))
            try:
                tag.save()
                i += 1
            except IntegrityError:
                self.stdout.write('Info: Tag DUPLICATION. Repeating #' + str(i))

                tag.text += '_or_' + str(i)
                tag.save()

        min_tag_pk, max_tag_pk = get_borders(Tag.objects.all())
        self.stdout.write(self.style.SUCCESS('Successfully generate %d tags' % options['tags_count']))

        i = 0
        while i < options['question_count']:
            question = Question(
                title=self.fake.sentence(nb_words=7, variable_nb_words=True,
                                         ext_word_list=None)[:-1] + '?',
                content=self.fake.text(max_nb_chars=520, ext_word_list=None),

                author=get_random_element(Profile.objects.all(), None,None))

            # answers=options['answers_to_one_count'])  # мы сейчас точно знаем, сколько будет ответов

            try:
                question.save()
                i += 1
            except IntegrityError:
                self.stdout.write('Info: Question DUPLICATION. Repeating #' + str(i))
                continue
            # while
            question.tags.add(get_random_element(Tag.objects.all(), None, None))
            question.tags.add(get_random_element(Tag.objects.all(), None, None))
            question.tags.add(get_random_element(Tag.objects.all(), None, None))

            for _ in range(options['answers_to_one_count']):
                answer = Answer(title=question.title, content=self.fake.text(max_nb_chars=250, ext_word_list=None),
                                author=get_random_element(Profile.objects, None, None), id=Answer.objects.count() + 1)

                answer.save()
                question.answers.add(answer)

            correct_answ = question.answers.all()[0]
            correct_answ.is_correct = True

            correct_answ.save()
            try:
                print('quest save')
                question.save()
                i += 1
            except IntegrityError:
                self.stdout.write('Info: Question DUPLICATION. Repeating #' + str(i))
                continue

        min_question_pk, max_question_pk = get_borders(Question.list.all())
        min_answer_pk, max_answer_pk = get_borders(Answer.objects.all())
        self.stdout.write(self.style.SUCCESS('Successfully generate %d questions' % options['question_count']))

        i = 0
        while i < options['votes_count']:
            i += 1

            if random.randint(0, 1):
                content = get_random_element(Question.list, None,None)
            else:
                content = get_random_element(Answer.objects.all(), None,None)

            vote = Vote(id=Vote.objects.count() + 1, author=get_random_element(Profile.objects, None, None))
            print(vote.id)
            vote.save()
            content.votes.add(vote)
            content.save()
        self.stdout.write(self.style.SUCCESS('Successfully generate %d votes' % options['votes_count']))

    def add_arguments(self, parser):
        parser.add_argument('user_count', nargs='?', type=int)
        parser.add_argument('question_count', nargs='?', type=int)
        parser.add_argument('tags_count', nargs='?', type=int)
        parser.add_argument('votes_count', nargs='?', type=int)
        parser.add_argument('answers_to_one_count', nargs='?', type=int)
