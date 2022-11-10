import sys, os
sys.path.append(os.path.abspath(os.pardir))
from django.views import View
from ..models import AccidentInvestigationCard, EventTimelineMemo
import json
from .utils import *


class EventMemo(View, TaskIDUtils):
    def get(self, request, task_id):
        memos = self.searching_memo(task_id)
        return JsonResponse(self.msg__memo_search_response(memos))

    def post(self, request, task_id):
        query = json.loads(request.body.decode('utf-8'))
        if 'memo_id' in query:
            memo = self.modify_memo(query)
        else:
            memo = self.create_memo(query, task_id)
        return JsonResponse(self.msg__memo_info(memo))

    def searching_memo(self, task_id):
        TaskIDUtils.__init__(self, task_id)
        task = self._get_task_from_task_id()

        q = EventTimelineMemo.objects.all()
        q = q.filter(car_id=task.car_id)
        q = q.filter(event_at__gte=task.investigation_start_time)
        q = q.filter(event_at__lte=task.investigation_end_time)
        q = q.filter(is_valid=True)

        return q

    @staticmethod
    def msg__memo_info(memo):

        return {
            'memo_id': memo.event_timeline_memo_id,
            'event_at': memo.event_at,
            'memo': memo.event_desc,
            'created_at': memo.event_desc_created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'modified_at': memo.event_desc_modified_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_accident': memo.is_accident
        }

    def msg__memo_search_response(self, memos):

        memo_data = []
        for memo in memos:
            memo_data.append(self.msg__memo_info(memo))

        return {
            'memo_data': memo_data,
        }

    @staticmethod
    def modify_memo(query):
        memo = EventTimelineMemo.objects.get(event_timeline_memo_id=int(query['memo_id']))
        memo.event_desc = query['memo']
        memo.event_at = string_to_utc(query['memo_at'])
        memo.event_desc_modified_at = datetime.now()
        if 'is_accident' in query:
            if query['is_accident'] == '0':
                memo.is_accident = False
            else:  # query['is_accident'] == '1':
                memo.is_accident = True
        memo.save()
        return memo

    def create_memo(self, query, task_id):
        TaskIDUtils.__init__(self, task_id)
        task = self._get_task_from_task_id()

        memo = EventTimelineMemo()
        memo.accident_investigation_card = AccidentInvestigationCard.objects.get(accident_investigation_card_id=task_id)
        memo.car_id = task.car_id
        memo.event_at = string_to_utc(query['memo_at'])
        memo.event_desc = query['memo']

        now = datetime.now()
        memo.event_desc_created_at = now
        memo.event_desc_modified_at = now
        memo.is_valid = True

        if 'is_accident' in query:
            if query['is_accident'] == '0':
                memo.is_accident = False
            else:  # query['is_accident'] == '1':
                memo.is_accident = True
        memo.save()

        return memo
