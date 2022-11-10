from ..models import AccidentInvestigationCard, Car, Manager
from datetime import datetime, timedelta
from django.http import JsonResponse


def add_kst_tz(string):
    return datetime.strptime(f"{string}+09:00", '%Y-%m-%d %H:%M:%S%z')


def string_to_utc(string):
    return datetime.strptime(f"{string}+00:00", '%Y-%m-%d %H:%M:%S%z')


class QueryUtils:
    def __init__(self, query):
        self.query = query
        self._parse_basic_info_in_query()

    def _parse_basic_info_in_query(self):
        self.task_id = None
        if 'task_id' in self.query:
            self.task_id = int(self.query['task_id'])

        self.car_id, self.car_num = None, None
        if 'car_id' in self.query:
            self.car_id = int(self.query['car_id'])
            self.car_num = Car.objects.get(car_id=self.car_id).car_num
        elif 'car_number' in self.query:
            self.car_id = Car.objects.get(car_num=self.query['car_number']).car_id
            self.car_num = self.query['car_number']

        self.start_at, self.end_at = None, None
        if 'start_at' in self.query:
            self.start_at, self.end_at = self.query['start_at'], self.query['end_at']
            if type(self.start_at) == str:
                self.start_at, self.end_at = string_to_utc(self.start_at), string_to_utc(self.end_at)

        self.manager_name, self.manager_id = None, None
        if 'manager' in self.query:
            self.manager_name = self.query['manager']
            if not Manager.objects.filter(manager_name=self.manager_name).exists():
                return JsonResponse({"message": "MANAGER_DOES_NOT_EXIST"}, status=400)
            manager = Manager.objects.get(manager_name=self.manager_name)
            self.manager_id = manager.manager_id

    def _return_available_date(self):
        self._parse_basic_info_in_query()
        date_arr = []
        cur_date = self.start_at
        while cur_date < self.end_at:
            date_arr.append(cur_date)
            cur_date = cur_date + timedelta(days=1)
        return date_arr


class TaskIDUtils:
    def __init__(self, task_id):
        self.task_id = task_id

    def _get_task_from_task_id(self):
        if not AccidentInvestigationCard.objects.filter(accident_investigation_card_id=self.task_id).exists():
            return JsonResponse({"message": "PRODUCT_DOES_NOT_EXIST"}, status=400)
        task = AccidentInvestigationCard.objects.get(accident_investigation_card_id=self.task_id)
        return task
