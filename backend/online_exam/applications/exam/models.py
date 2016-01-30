import uuid
from datetime import datetime
from django.db import models
from applications.core.models import TimeStampedModel
from applications.user.models import User

DIFFICULTY_CHOICES = (
    (1, 'Easy'),
    (2, 'Normal'),
    (3, 'Hard')
)


class Exam(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=30)
    description = models.TextField()

    duration = models.DurationField()

    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)

    available = models.BooleanField(default=False)
    available_start = models.DateTimeField(blank=True, null=True)
    available_end = models.DateTimeField(blank=True, null=True)

    questions = models.ManyToManyField(
        'quiz.Question', related_name='questions')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.available_start:
            self.available_start = datetime.now()
        if not self.available_end and self.available_start:
            self.available_end = self.available_start + self.duration
        super().save(*args, **kwargs)


class ExamScore(TimeStampedModel):
    user = models.ForeignKey(User)
    exam = models.ForeignKey(Exam)
    score = models.FloatField()
    duration = models.DurationField()

    def __str__(self):
        return "%s: %.2f" % (self.user.get_full_name(), self.score)
