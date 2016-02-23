from django import template
from applications.quiz.models import QuestionAnswerUser

register = template.Library()


@register.filter
def is_answered(question_id, user_id):
    return QuestionAnswerUser.objects.filter(
        question_id=question_id, user_id=user_id).exists()
