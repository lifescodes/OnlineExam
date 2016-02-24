from django import template
from applications.quiz.models import QuestionAnswerUser

register = template.Library()


@register.filter
def is_answered(choice_id, user_id):
    return QuestionAnswerUser.objects.filter(
        choice_id=choice_id, user_id=user_id).exists()
