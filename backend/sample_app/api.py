from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone, dateparse

from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import *
from datetime import datetime, timedelta
import json
import boto3
from io import BytesIO
import pandas as pd
import numpy as np

client = boto3.client(
    's3',
    aws_access_key_id='ASIASPOWPLBFOG6FDL4T',
    aws_secret_access_key='aEwuhD143O/TJ7dRHOPjeVJmUL48h6treGX77ODi',
    aws_session_token="IQoJb3JpZ2luX2VjEHEaDmFwLW5vcnRoZWFzdC0yIkcwRQIhAJ4MBQqBmsjd6wQ5aCShTCOb0J1Z9lupWqVJ1XY66ONNAiAY/vLXT4wXbjGJEnCQgn/simPIRzJ3OrNUrtzeyl8EjCrgAghqEAEaDDE3MDYzNzg3NTI3NCIMFJZcEWVhswvkvLO2Kr0CoFMhm5HnxhG0N1JBe7NQjHePZ18Cj97LpeLkdpjforne/7qYvDsHz08HR81lf8+EzMzBT2by+qpQel6gIER427GzlTU5RRNMvMO+gZNII7jrjApkrjHdIt7Z1YXYoXcNkSyPbsUkQc2Sbbx3dr1ZfczIfRQkJhd6znT0Z2PeH6l2PyUQtmqIHpnWQAn98aq2NqrYAXfa0jqTTnF6G0Dnba7Ku9K9dUM/bGzJZNXmHjxaUJTnNS/9VKOYmkf72w8pvi5Py6XnZ9lQhJAh3DZppQ0y9pT45G/8RE7b2kgHU2A0SQ9I5nYhxhu7R593liweOwyPnW3AZ6EgPPHW83PGa+qk9Z8bTMRcIAgeXWGs2LaVwirxxZ7tn/CuaaKxMoipFWcx430jI1idjCO2Kzl2yVDc/8BX/ajgPQqSn9YwwZ6xmwY6nQESQ0xuQVO1IMdkuhjD/5iVnmQ4ys29R1lInJ/t/mwfDtVrUfhmKW6SbVaYesj52BJ1OC0kmFQAscdU/FUkvzg1wi/18ju0cSyXh5kkIdxwSH90seU1T0mz+oITwytk06PGghliNq9ZNCqgW6vS9pfywi0jCM/n4rVdLizd+TrfBmqBqPSkKg8YV7G3E6SEQh3ookXWqBgSY6CMEN1v"
)

print('hello')

bucket_name = '42dot-umos-dev-solution'
PREFIX_MOVIE = 'accident_reconstruction_demo/movie'
PREFIX_SENSORDATA = 'accident_reconstruction_demo/sensor_data'


def create_presigned_url(client, bucket_name, object_name, expiration=3600):
    response = client.generate_presigned_url('get_object',
                                             Params={'Bucket': bucket_name,
                                                    'Key': object_name},
                                             ExpiresIn=expiration)
    return response  # url string



# path('task/', api.task), #
# path('task/<int:task_id>/', api.to_taskpage), #
# path('movie/', api.handle_movie_info), #
# path('timerange/', api.check_timerange),  # --
# path('task/<int:task_id>/movie/', api.get_movie), #
# path('task/<int:task_id>/trajectory/', api.get_trajectory),
# path('task/<int:task_id>/sensor-imu/', api.get_sensor_imu),
# path('task/<int:task_id>/event-timeline/', api.handle_event_timeline), #



def index(request):
    return HttpResponse("안녕하세요 Accident Reconstruction에 오신것을 환영합니다.")


def searching_task(query):
    # class AccidentInvestigationCard(models.Model):
    #     accident_investigation_card_id = models.AutoField(primary_key=True)  -> task_id
    #     manager_id = models.IntegerField()  -> manager
    #     car = models.ForeignKey('Car', models.DO_NOTHING) -> car_number를 이용해서 car_id를 가져와야함
    #     driver = models.ForeignKey('Driver', models.DO_NOTHING) -> Not Used For Query
    #     investigation_start_time = models.DateTimeField() -> start_at
    #     investigation_end_time = models.DateTimeField() -> end_at
    #     work_done = models.BooleanField() -> status
    #     card_made_by = models.ForeignKey('Manager', models.DO_NOTHING) -> created_by
    #     memo = models.TextField(blank=True, null=True) -> Not Used For Query
    #     is_accident = models.IntegerField(blank=True, null=True) -> is_accident
    #
    #     class Meta:
    #         managed = False
    #         db_table = 'accident_investigation_card'

    q = AccidentInvestigationCard.objects.all()

    if 'task_id' in query:
        q = q.filter(accident_investigation_card_id=query['task_id'])

    if 'manager' in query:
        manager = Manager.objects.get(manager_name=query['manager'])
        q = q.filter(manager_id=manager.manager_id)

    if 'car_number' in query:
        car = Car.objects.get(car_num=query['car_number'])
        q = q.filter(car=car.car_id)

    if 'start_at' in query:
        q = q.filter(investigation_end_time__gte=datetime.strptime(query['start_at'], '%Y-%m-%d %H:%M:%S'))

    if 'end_at' in query:
        q = q.filter(investigation_start_time__lte=datetime.strptime(query['end_at'], '%Y-%m-%d %H:%M:%S'))

    if 'status' in query:
        if query['status'] == '대기 중':
            q = q.filter(work_done__isnull=True)
        elif query['status'] == '확인 중':
            q = q.filter(work_done=False)
        else:  # query['status'] == '확인 완료'
            q = q.filter(work_done=True)

    if 'created_by' in query:
        if query['created_by'] == '0':  # AI. 긴급
            q = q.filter(card_made_by__manager_name__startswith='AI.emergency')

        elif query['created_by'] == '1':  # AI. 일반
            q = q.filter(card_made_by__manager_name__startswith='AI.common')

        else:
            q = q.exclude(card_made_by__manager_name__startswith='AI.emergency')
            q = q.exclude(card_made_by__manager_name__startswith='AI.common')

    if 'is_accident' in query:
        if query['is_accident'] == "0":  # 사고 아님(을 확인)
            q = q.filter(work_done=True)
            q = q.filter(is_accident=0)

        elif query['is_accident'] == "1":  # 사고(임을 확인)
            q = q.filter(work_done=True)
            q = q.filter(is_accident=100)

        else:  # query['is_accident'] == "2":
            q = q.exclude(work_done=True)

    return q


def msg__task_search_response(tasks):

    task_data = []
    for task in tasks:
        task_data.append(msg__task_info(task))

    return {
        'task_data': task_data,
        'total_tasks': len(tasks)
    }


def msg__task_info(task):
    def msg__card_made_by(card_made_by):
        print(card_made_by.manager_name)
        print(type(card_made_by.manager_name))
        if card_made_by.manager_name.startswith('AI.emergency'):
            return 'AI-긴급'
        elif card_made_by.manager_name.startswith('AI.common'):
            return 'AI-일반'
        else:
            return card_made_by.manager_name

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

    def msg__status(work_done):
        msg = ''
        if work_done is None:  # 대기 중
            msg = "대기 중"
        elif not work_done:  # 확인 중
            msg = "확인 중"
        elif work_done:  # 확인 완료
            msg = '확인 완료'
        return msg

    return {
        'task_id': task.accident_investigation_card_id,
        'car_id': task.car.car_id,
        'car_number': task.car.car_num,
        'manager': Manager.objects.get(manager_id=task.manager_id).manager_name,
        'status': msg__status(task.work_done),
        'start_at': task.investigation_start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_at': task.investigation_end_time.strftime('%Y-%m-%d %H:%M:%S'),
        'created_by': msg__card_made_by(task.card_made_by),
        'is_accident': msg__is_accident(task),
        'created_at': task.card_created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': task.card_updated_at.strftime('%Y-%m-%d %H:%M:%S')
    }


def msg__task_create_response(new_task):
    return msg__task_info(new_task)


def create_new_task(query):
    new_card = AccidentInvestigationCard()

    the_manager = Manager.objects.get(manager_name=query['manager'])
    new_card.manager_id = the_manager.manager_id
    new_card.car = Car.objects.get(car_num=query['car_number'])
    new_card.driver = Driver.objects.get(driver_id=1)  # TODO: 추후 예약정보를 조회하여 어떤 사람이 운전하였는지 조사

    now = timezone.now()
    new_card.card_created_at = now
    new_card.card_updated_at = now

    new_card.investigation_start_time = datetime.strptime(query['start_at'], '%Y-%m-%d %H:%M:%S')
    new_card.investigation_end_time = datetime.strptime(query['end_at'], '%Y-%m-%d %H:%M:%S')

    new_card.work_done = False
    new_card.card_made_by = the_manager
    new_card.memo = ''

    new_card.save()

    return new_card


def task(request):
    query = json.loads(request.body.decode('utf-8'))
    print(query)

    if request.method == 'GET':
        tasks = searching_task(query)
        return JsonResponse(msg__task_search_response(tasks))

    if request.method == 'POST':
        new_task = create_new_task(query)
        return JsonResponse(msg__task_create_response(new_task))


def to_taskpage(request, task_id):
    if request.method == 'GET':
        task = AccidentInvestigationCard.objects.get(accident_investigation_card_id=task_id)
        return JsonResponse(msg__task_info(task))


def find_movie(query):
    if 'car_id' in query:
        car_id = int(query['car_id'])
    else:
        car = Car.objects.get(car_num=query['car_number'])
        car_id = car.car_id

    if type(query['start_at']) == str:
        start_at = datetime.strptime(query['start_at'] + '+0000', '%Y-%m-%d %H:%M:%S%z')
        end_at = datetime.strptime(query['end_at'] + '+0000', '%Y-%m-%d %H:%M:%S%z')
    else:
        start_at = query['start_at']
        end_at = query['end_at']

    movie = BlackboxMovie.objects.all()
    movie = movie.filter(car_id=car_id)
    movie = movie.filter(movie_start_at__lte=end_at)
    movie = movie.filter(movie_end_at__gte=start_at)

    return movie


def find_sensor_data_key(query):
    car_id = query['car_id']
    start_at = query['start_at'] - timedelta(minutes=2)  # 센서데이터가 최대 몇분 주기로 올라오는지 확인하고 버퍼 주기
    end_at = query['end_at']

    date_arr = []
    cur_date = start_at
    while cur_date < end_at:
        date_arr.append(cur_date)
        cur_date = cur_date + timedelta(days=1)

    prefixes = [f"{PREFIX_SENSORDATA}/{car_id:08}/{day.strftime('%Y%m/%d/')}" for day in date_arr]

    paginator = client.get_paginator('list_objects_v2')

    obj_keys = []
    for prefix in prefixes:
        pages = paginator.paginate(Bucket=bucket_name,
                                   Prefix=prefix)
        for page in pages:
            if 'Contents' in page:
                obj_keys.extend([obj['Key'] for obj in page['Contents']])

    data_match = []
    for key in obj_keys:
        filename = key.rsplit('/')[-1]
        yyyymmdd1, hhmmss1, yyyymmdd2, hhmmss2, _ = filename.split('_', 4)
        data_start_at = datetime.strptime(yyyymmdd1 + hhmmss1+'+0000', '%Y%m%d%H%M%S%z')
        data_end_at = datetime.strptime(yyyymmdd2 + hhmmss2 + '+0000', '%Y%m%d%H%M%S%z')

        if (data_start_at < end_at) and (start_at < data_end_at):
            data_match.append(key)

    return data_match


def handle_movie_info(request):
    query = json.loads(request.body.decode('utf-8'))
    if request.method == 'GET':
        # query = {
        #     "car_number": "001허0001",
        #     "start_at": "2022-09-07 11:55:00",
        #     "end_at": "2022-09-07 12:10:00"
        movies = find_movie(query)
        query['number_total_movie'] = len(movies)
        return JsonResponse(query)


def label_movie(request, movie_id):
    query = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        # query = {
        #     "car_id": "1",
        #     "manager": "suhyun.kim",
        #     "label": 1
        # }
        print(query)
        print(f"movie_id: {movie_id}")
        movie = BlackboxMovie.objects.get(blackbox_movie_id=movie_id)
        manager = Manager.objects.get(manager_name=query['manager'])
        if BlackboxMovieLabelInfo.objects.filter(
                blackbox_movie_id=movie.blackbox_movie_id,
                labeler_id=manager.manager_id
        ).exists():
            # 수정
            print('label modified')
            movie_label = BlackboxMovieLabelInfo.objects.filter(
                blackbox_movie_id=movie.blackbox_movie_id,
                labeler_id=manager.manager_id
            )

            movie_label = movie_label[0]
            movie_label.is_accident = int(query['label']) if int(query['label']) >= 0 else None
            now = timezone.now()
            movie_label.label_modified_at = now
            movie_label.save()

            query['label_created_at'] = movie_label.label_created_at.strftime('%Y-%m-%d %H:%M:%S')
            query['label_modified_at'] = now.strftime('%Y-%m-%d %H:%M:%S')

        else:
            # 생성
            print('label created')
            movie_label = BlackboxMovieLabelInfo()
            movie_label.blackbox_movie_id = movie.blackbox_movie_id
            movie_label.labeler = manager
            movie_label.is_accident = int(query['label']) if int(query['label']) > 0 else None
            now = timezone.now()
            movie_label.label_created_at = now
            movie_label.label_modified_at = now

            movie_label.save()

            query['label_created_at'] = now.strftime('%Y-%m-%d %H:%M:%S')
            query['label_modified_at'] = now.strftime('%Y-%m-%d %H:%M:%S')

        return JsonResponse(query)


# def check_timerange(request):
#     return HttpResponse("안녕하세요 Accident Reconstruction에 오신것을 환영합니다.")


def get_movie(request, task_id):
    if request.method == 'GET':
        task = AccidentInvestigationCard.objects.get(accident_investigation_card_id=task_id)
        start_at = task.investigation_start_time
        end_at = task.investigation_end_time
        query = {
            'car_id': task.car_id,
            'start_at': start_at,
            'end_at': end_at
        }
        movies = find_movie(query)

        movie_ids, presigned_urls, movie_names, movie_start_at_list, movie_end_at_list = [], [], [], [], []
        movie_label_list = []
        for movie in movies:
            movie_ids.append(movie.blackbox_movie_id)
            mname = movie.blackbox_movie_name
            key = f"accident_reconstuction_demo/{task.car_id:08d}/{mname[0:6]}/{mname[6:8]}/{mname.split('_')[2]}/{mname}"
            presigned_urls.append(
                create_presigned_url(client, bucket_name, key)
            )
            movie_names.append(mname)
            movie_start_at_list.append(movie.movie_start_at.strftime('%Y-%m-%d %H:%M:%S'))
            movie_end_at_list.append(movie.movie_end_at.strftime('%Y-%m-%d %H:%M:%S'))

            if BlackboxMovieLabelInfo.objects.filter(blackbox_movie_id=movie.blackbox_movie_id).exists():
                movie_label = BlackboxMovieLabelInfo.objects.filter(
                    blackbox_movie_id=movie.blackbox_movie_id,
                ).order_by('-label_modified_at')
                label = movie_label[0].is_accident
                label = label if label is not None else -1
            else:
                label = -1
            movie_label_list.append(label)

        return JsonResponse({
            'task_id': task_id,
            'presigned_url_list': presigned_urls,
            'movie_name_list': movie_names,
            'movie_id_list': movie_ids,
            'movie_start_at_list': movie_start_at_list,
            'movie_end_at_list': movie_end_at_list,
            'movie_label_list' : movie_label_list
        })


def get_csv_data(client, key):
    resp = client.get_object(Bucket=bucket_name, Key=key)
    df = pd.read_csv(BytesIO(resp['Body'].read()))
    return df


def get_trajectory(request, task_id):
    if request.method == 'GET':
        task = AccidentInvestigationCard.objects.get(accident_investigation_card_id=task_id)
        start_at = task.investigation_start_time
        end_at = task.investigation_end_time
        query = {
            'car_id': task.car_id,
            'start_at': start_at,
            'end_at': end_at
        }
        sensor_data_keys = find_sensor_data_key(query)
        sensor_data_keys = [key for key in sensor_data_keys if not ('100Hz' in key)]  # 100Hz는 일단 제외

        dfs = [get_csv_data(client, key) for key in sensor_data_keys]

        df = pd.concat(dfs, ignore_index=True)
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        df.sort_values(by='Datetime', ignore_index=True, inplace=True)
        df.set_index('Datetime', inplace=True)

        index_sample = pd.date_range(
            df.index[0],
            periods=np.ceil((df.index[-1] - df.index[0]) / timedelta(seconds=1)),
            freq="1S")

        latlng = df[['lat', 'lng']].asof(index_sample)

        ts_array = []
        coord_array = []
        for i, row in latlng.iterrows():
            ts_array.append(i.strftime('%Y-%m-%d %H:%M:%S'))
            # ts_array.append(i)
            coord_array.append([np.round(row.lat, 7), np.round(row.lng, 7)])  # GPS 7자리 = 1.11cm

        polyline = {
              "type": "Feature",
              "geometry": {
                "type": "LineString",
                "coordinates": coord_array
              },
              "properties": {
                "timestamp": ts_array
              }
        }

        return JsonResponse({
            'task_id': task.accident_investigation_card_id,
            'car_id': task.car_id,
            'car_number': Car.objects.get(car_id=task.car_id).car_num,
            'polyline': polyline,
            'start_at': start_at,
            'end_at': end_at
        })


def get_sensor_imu(request, task_id):
    if request.method == 'GET':
        task = AccidentInvestigationCard.objects.get(accident_investigation_card_id=task_id)
        start_at = task.investigation_start_time
        end_at = task.investigation_end_time
        query = {
            'car_id': task.car_id,
            'start_at': start_at,
            'end_at': end_at
        }
        sensor_data_keys = find_sensor_data_key(query)
        sensor_data_keys = [key for key in sensor_data_keys if ('100Hz' in key)]  # 100Hz는 일단 제외
        dfs = [get_csv_data(client, key) for key in sensor_data_keys]
        df = pd.concat(dfs, ignore_index=True)
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        df.sort_values(by='Datetime', ignore_index=True, inplace=True)
        df.set_index('Datetime', inplace=True)
        df.dropna(inplace=True)
        xAccel = np.round(df['mLocalAccelx'].to_numpy(), 1).tolist()
        yAccel = np.round(df['mLocalAccely'].to_numpy(), 1).tolist()
        zAccel = np.round(df['mLocalAccelz'].to_numpy(), 1).tolist()
        timestamp = [ts.strftime('%Y-%m-%d %H:%M:%S') for ts in df.index]

        return JsonResponse({
            'car_id': task.car_id,
            'timestmap': timestamp,
            'xAccel': xAccel,
            'yAccel': yAccel,
            'zAccel': zAccel,
            'start_at': start_at,
            'end_at': end_at
        })


def searching_memo(task_id):
    task = AccidentInvestigationCard.objects.get(accident_investigation_card_id=task_id)

    q = EventTimelineMemo.objects.all()
    q = q.filter(car_id=task.car_id)
    q = q.filter(event_at__gte=task.investigation_start_time)
    q = q.filter(event_at__lte=task.investigation_end_time)
    q = q.filter(is_valid=True)

    return q


def msg__memo_info(memo):
    # event_timeline_memo_id = models.AutoField(primary_key=True)
    # accident_investigation_card = models.ForeignKey(AccidentInvestigationCard, models.DO_NOTHING, blank=True, null=True)
    # car_id = models.IntegerField()
    # event_at = models.DateTimeField()
    # event_desc = models.TextField()
    # event_desc_created_at = models.DateTimeField()
    # event_desc_modified_at = models.DateTimeField(blank=True, null=True)
    # is_valid = models.BooleanField()
    # is_accident = models.IntegerField(blank=True, null=True)
    return {
        'memo_id': memo.event_timeline_memo_id,
        'event_at': memo.event_at,
        'memo': memo.event_desc,
        'created_at': memo.event_desc_created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'modified_at': memo.event_desc_modified_at.strftime('%Y-%m-%d %H:%M:%S'),
        'is_accident': memo.is_accident
    }


def msg__memo_search_response(memos):

    memo_data = []
    for memo in memos:
        memo_data.append(msg__memo_info(memo))

    return {
        'memo_data': memo_data,
    }


def modify_memo(query):
    memo = EventTimelineMemo.objects.get(event_timeline_memo_id=int(query['memo_id']))
    memo.event_desc = query['memo']
    memo.event_at = datetime.strptime(query['memo_at'], '%Y-%m-%d %H:%M:%S')
    memo.event_desc_modified_at = timezone.now()
    if 'is_accident' in query:
        if query['is_accident'] == '0':
            memo.is_accident = False
        else:  # query['is_accident'] == '1':
            memo.is_accident = True
    memo.save()
    return memo


def create_memo(query, task_id):
    task = AccidentInvestigationCard.objects.get(accident_investigation_card_id=task_id)

    memo = EventTimelineMemo()
    memo.accident_investigation_card = AccidentInvestigationCard.objects.get(accident_investigation_card_id=task_id)
    memo.car_id = task.car_id
    memo.event_at = datetime.strptime(query['memo_at'], '%Y-%m-%d %H:%M:%S')
    memo.event_desc = query['memo']

    now = timezone.now()
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


def handle_event_timeline(request, task_id):
    if request.method == 'GET':
        memos = searching_memo(task_id)
        return JsonResponse(msg__memo_search_response(memos))

    if request.method == 'POST':
        query = json.loads(request.body.decode('utf-8'))
        print(query)
        if 'memo_id' in query:
            memo = modify_memo(query)
            return JsonResponse(msg__memo_info(memo))
        else:
            memo = create_memo(query, task_id)
            return JsonResponse(msg__memo_info(memo))

