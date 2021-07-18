from django.utils import timezone

from apps.csat.models import ApplicationQuestion


def update_question(data):
    for d in data:
        if len(d['answer']) > 1:
            answer = ''
            for i in d['answer']:
                id = i['answer_option']
                answer += i['answer_option'] + ', '

        else:
            id = d['answer'][0]['id']
            answer = d['answer'][0]['answer_option']
        question_id = d['question_id']
        time_to_answer = d['time_to_answer']
        date_answer = d['date_answer']
        app_question = ApplicationQuestion.objects.filter(
            id=question_id
        ).update(
            time_to_answer=time_to_answer,
            answer=answer,
            date_answer=date_answer,
            changed_at=timezone.localtime()
        )
    return True