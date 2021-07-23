from django.utils import timezone

from apps.csat.models import ApplicationQuestion
from apps.users.models import User


def update_question(data):
    user_query = User.objects.all()
    ques = ApplicationQuestion.objects.select_related('application')

    for d in data:
        if len(d['answer']) > 1:
            answer = ''
            for i in d['answer']:
                id = i['answer_option']
                answer += i['answer_option'] + ', '

        else:
            answer = d['answer'][0]['answer_option']

        question_id = d['question_id']
        time_to_answer = d['time_to_answer']
        date_answer = d['date_answer']

        user = user_query.filter(id=d['person_id']).first()
        app_question = ques.filter(
            id=question_id,
            application__user_forms__user=user,
            application__uuid=d['uuid']
        ).update(
            time_to_answer=time_to_answer,
            answer=answer,
            date_answer=date_answer,
            changed_at=timezone.localtime()
        )
    return True