import sys, os
sys.path.append(os.path.abspath(os.pardir))

from django.views import View
from .utils import *
from library.s3_libs import AmazonWebService as AWS
from dotenv import load_dotenv
from io import BytesIO
import pandas as pd
import numpy as np

load_dotenv()

PREFIX_SENSORDATA = os.getenv("PREFIX_SENSORDATA")
BUCKET_NAME = os.getenv("BUCKET_NAME")
aws = AWS(bucket_name=BUCKET_NAME)


class SensorUtils(QueryUtils, TaskIDUtils):
    @staticmethod
    def get_csv_data(key):
        resp = aws.get_object(key)
        df = pd.read_csv(BytesIO(resp['Body'].read()))
        return df

    def _find_sensor_data_key_by_query(self, query):
        QueryUtils.__init__(self, query)
        self._parse_basic_info_in_query()
        self.start_at -= timedelta(minutes=2)
        date_arr = self._return_available_date()

        prefixes = [f"{PREFIX_SENSORDATA}/{self.car_id:08}/{day.strftime('%Y%m/%d/')}" for day in date_arr]
        obj_keys = [obj for prefix in prefixes for obj in aws.s3_list_objects(prefix=prefix)]

        data_match = []
        for key in obj_keys:
            yyyymmdd1, hhmmss1, yyyymmdd2, hhmmss2, _ = key.rsplit('/')[-1].split('_', 4)
            sensor_data_start_at = datetime.strptime(yyyymmdd1 + hhmmss1 + '+0000', '%Y%m%d%H%M%S%z')
            sensor_data_end_at = datetime.strptime(yyyymmdd2 + hhmmss2 + '+0000', '%Y%m%d%H%M%S%z')
            if (sensor_data_start_at < self.end_at) and (self.start_at < sensor_data_end_at):
                data_match.append(key)

        return data_match

    def _preprocess_sensor_data(self, task_id):
        TaskIDUtils.__init__(self, task_id)
        self.task = self._get_task_from_task_id()
        start_at = self.task.investigation_start_time
        end_at = self.task.investigation_end_time
        query = {
            'car_id': self.task.car_id,
            'start_at': start_at,
            'end_at': end_at
        }

        sensor_data_keys = self._find_sensor_data_key_by_query(query)
        sensor_data_keys = [key for key in sensor_data_keys if not ('100Hz' in key)]  # 100Hz는 일단 제외

        dfs = [self.get_csv_data(key) for key in sensor_data_keys]

        if not len(dfs):
            return None

        df = pd.concat(dfs, ignore_index=True)
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        df.sort_values(by='Datetime', ignore_index=True, inplace=True)
        df.set_index('Datetime', inplace=True)

        return df


class SensorIMU(View, SensorUtils):
    def get(self, request, task_id):

        df = self._preprocess_sensor_data(task_id)
        df.dropna(inplace=True)
        x_accel = np.round(df['mLocalAccelx'].to_numpy(), 1).tolist()
        y_accel = np.round(df['mLocalAccely'].to_numpy(), 1).tolist()
        z_accel = np.round(df['mLocalAccelz'].to_numpy(), 1).tolist()
        timestamp = [ts.strftime('%Y-%m-%d %H:%M:%S') for ts in df.index]

        return JsonResponse({
            'car_id': self.task.car_id,
            'timestmap': timestamp,
            'xAccel': x_accel,
            'yAccel': y_accel,
            'zAccel': z_accel,
            'start_at': self.start_at,
            'end_at': self.end_at
        })


class Trajectory(View, SensorUtils):
    def get(self, request, task_id):
        df = self._preprocess_sensor_data(task_id)

        if df is None:
            return JsonResponse({
                'task_id': self.task.accident_investigation_card_id,
                'car_id': self.task.car_id,
                'car_number': Car.objects.get(car_id=self.task.car_id).car_num,
                'polyline': None,  # TODO: 명세서에 표시
                'start_at': self.start_at,
                'end_at': self.end_at
            })

        index_sample = pd.date_range(
            df.index[0],
            periods=np.ceil((df.index[-1] - df.index[0]) / timedelta(seconds=1)),
            freq="1S")

        latlng = df[['lat', 'lng']].asof(index_sample)

        ts_array, coord_array = [], []

        for i, row in latlng.iterrows():
            ts_array.append(i.strftime('%Y-%m-%d %H:%M:%S'))
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
            'task_id': self.task.accident_investigation_card_id,
            'car_id': self.task.car_id,
            'car_number': Car.objects.get(car_id=self.task.car_id).car_num,
            'polyline': polyline,
            'start_at': self.start_at,
            'end_at': self.end_at
        })