from django.views import View
import json
from .utils import *


class QueryToTask(QueryUtils):
    def __init__(self, query):
        QueryUtils.__init__(self, query)

    def _search_task_by_query(self):
        key_filter_dict = {
            self.task_id: 'accident_investigation_card_id',
            self.start_at: 'investigation_end_time__gte',
            self.end_at: 'investigation_start_time__lte',
            self.manager_id: 'manager_id',
            self.car_id: 'car_id'
        }

        filtered_query = AccidentInvestigationCard.objects.all()
        for query_value, filter_key in key_filter_dict.items():
            if query_value is not None:
                filtered_query = eval(f"filtered_query.filter({filter_key}={query_value})")

        if 'status' in self.query:
            if self.query['status'] == '대기 중':
                filtered_query = filtered_query.filter(work_done__isnull=True)
            elif self.query['status'] == '확인 중':
                filtered_query = filtered_query.filter(work_done=False)
            else:  # query['status'] == '확인 완료'
                filtered_query = filtered_query.filter(work_done=True)

        if 'created_by' in self.query:
            if self.query['created_by'] == '0':  # AI. 긴급
                filtered_query = filtered_query.filter(card_made_by__manager_name__startswith='AI.emergency')

            elif self.query['created_by'] == '1':  # AI. 일반
                filtered_query = filtered_query.filter(card_made_by__manager_name__startswith='AI.common')

            else:
                filtered_query = filtered_query.exclude(card_made_by__manager_name__startswith='AI.emergency')
                filtered_query = filtered_query.exclude(card_made_by__manager_name__startswith='AI.common')

        if 'is_accident' in self.query:
            if self.query['is_accident'] == "0":  # 사고 아님(을 확인)
                filtered_query = filtered_query.filter(work_done=True)
                filtered_query = filtered_query.filter(is_accident=0)

            elif self.query['is_accident'] == "1":  # 사고(임을 확인)
                filtered_query = filtered_query.filter(work_done=True)
                filtered_query = filtered_query.filter(is_accident=100)

            else:  # query['is_accident'] == "2":
                filtered_query = filtered_query.exclude(work_done=True)

        return filtered_query

    def _create_task_by_query(self):
        new_card = AccidentInvestigationCard()
        the_manager = Manager.objects.get(manager_id=self.manager_id)
        new_card.manager_id = self.manager_id

        new_card.car = Car.objects.get(car_num=self.car_num)
        new_card.driver = Driver.objects.get(driver_id=1)  # TODO: 추후 예약정보를 조회하여 어떤 사람이 운전하였는지 조사

        now = datetime.now().astimezone()
        new_card.card_created_at = now
        new_card.card_updated_at = now

        new_card.investigation_start_time = self.start_at
        new_card.investigation_end_time = self.end_at

        new_card.work_done = False
        new_card.card_made_by = the_manager
        new_card.memo = ''

        new_card.save()

        return new_card


class TaskToResponse():
    def msg__task_info(self, task):
        return {
            'task_id': task.accident_investigation_card_id,
            'car_id': task.car.car_id,
            'car_number': task.car.car_num,
            'manager': task.manager_id,
            'status': self.msg__status(task.work_done),
            'start_at': task.investigation_start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_at': task.investigation_end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'created_by': self.msg__card_made_by(task.card_made_by),
            'is_accident': self.msg__is_accident(task),
            'created_at': task.card_created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': task.card_updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    @staticmethod
    def msg__card_made_by(card_made_by):
        if card_made_by.manager_name.startswith('AI.emergency'):
            return 'AI-긴급'
        elif card_made_by.manager_name.startswith('AI.common'):
            return 'AI-일반'
        return card_made_by.manager_name

    @staticmethod
    def msg__is_accident(task):
        msg = ''
        if task.work_done is None:  # 대기 중
            msg = f"({task.is_accident}%)"
        elif not task.work_done:  # 확인 중
            msg = '-'
        elif task.work_done:  # 확인 완료
            if task.is_accident == 0:
                msg = 'X'
            elif task.is_accident == 100:
                msg = 'O'
        return msg

    @staticmethod
    def msg__status(work_done):
        status = {
            None: "대기 중",
            True: "확인 중",
            False: "확인 완료"
        }
        return status[work_done]


class Task(View, TaskToResponse, QueryToTask):
    def get(self, request, *args, **kwargs):
        query = json.loads(request.body.decode('utf-8'))
        QueryToTask.__init__(self, query=query)
        tasks = self._search_task_by_query()
        return JsonResponse(self.msg__task_search_response(tasks))

    def post(self, request, *args, **kwargs):
        query = json.loads(request.body.decode('utf-8'))
        QueryToTask.__init__(self, query=query)
        new_task = self._create_task_by_query()
        return JsonResponse(self.msg__task_create_response(new_task))

    def msg__task_search_response(self, tasks):
        task_data = [self.msg__task_info(task) for task in tasks]
        return {
            'task_data': task_data,
            'total_tasks': len(task_data)
        }

    def msg__task_create_response(self, new_task):
        return self.msg__task_info(new_task)


class ToTaskPage(View, TaskToResponse, TaskIDUtils):
    def get(self, request, task_id):
        TaskIDUtils.__init__(self, task_id)
        task = self. _get_task_from_task_id()
        return JsonResponse(self.msg__task_info(task))