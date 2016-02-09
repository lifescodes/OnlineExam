from django.db import models

from applications.core.models import TimeStampedModel
from applications.exam.models import Exam
from applications.user.models import User

TYPE_CHOICES = (
    (1, 'Single'),
    (2, 'Multiple')
)


class Question(TimeStampedModel):
    exam = models.ForeignKey(Exam)
    text = models.TextField()
    position = models.IntegerField()
    question_type = models.IntegerField(choices=TYPE_CHOICES)

    def __str__(self):
        return self.exam.title


class QuestionAnswer(models.Model):
    question = models.ForeignKey(Question, related_name='answers')
    text = models.TextField()
    choice = models.CharField(max_length=1)
    correct = models.BooleanField(default=False)


class QuestionAnswerUser(TimeStampedModel):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    choice = models.ForeignKey(QuestionAnswer)
