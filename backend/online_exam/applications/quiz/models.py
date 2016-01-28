from django.db import models

from applications.core.models import TimeStampedModel
from applications.exam.models import Exam

TYPE_CHOICES = (
    (1, 'Single'),
    (2, 'Multiple')
)


class Question(TimeStampedModel):
    exam = models.ForeignKey(Exam)
    text = models.TextField()
    question_type = models.IntegerField(choices=TYPE_CHOICES)


class QuestionAnswer(models.Model):
    question = models.ForeignKey(Question)
    text = models.TextField()
    correct = models.BooleanField(default=False)
