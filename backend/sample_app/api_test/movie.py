import sys, os
sys.path.append(os.path.abspath(os.pardir))

from django.views import View
from .utils import *
from library.s3_libs import AmazonWebService as AWS
from dotenv import load_dotenv


load_dotenv()

PREFIX_MOVIE = os.getenv("PREFIX_MOVIE")
PREFIX_SENSORDATA = os.getenv("PREFIX_SENSORDATA")
BUCKET_NAME = os.getenv("BUCKET_NAME")
aws = AWS(bucket_name=BUCKET_NAME)


class Movie(View, QueryUtils, TaskIDUtils):
    def get(self, request, task_id):
        TaskIDUtils.__init__(self, task_id)
        task = self._get_task_from_task_id()

        query = {
            'car_id': task.car_id,
            'start_at': task.investigation_start_time,
            'end_at': task.investigation_end_time
        }

        movie_keys = self._find_movie_key_by_query(query)
        presigned_urls = [aws.create_presigned_url(key) for key in movie_keys]
        movie_names = [key.rsplit('/', 1)[-1] for key in movie_keys]

        return JsonResponse({
            'task_id': task_id,
            'presigned_url_list': presigned_urls,
            'movie_name_list': movie_names
        })

    def _find_movie_key_by_query(self, query):
        QueryUtils.__init__(self, query)
        self._parse_basic_info_in_query()
        date_arr = self._return_available_date()

        prefixes = [f"{PREFIX_MOVIE}/{self.car_id:08}/{day.strftime('%Y%m/%d/normal')}" for day in date_arr]
        obj_keys = [obj for prefix in prefixes for obj in aws.s3_list_objects(prefix=prefix)]

        movie_match = []
        for key in obj_keys:
            yyyymmdd, hhmmss, _ = key.rsplit('/')[-1].split('_', 2)
            movie_start_at = datetime.strptime(yyyymmdd + hhmmss + '+0000', '%Y%m%d%H%M%S%z')
            if self.start_at < movie_start_at < self.end_at:
                # TODO: 영상의 시작시간은 start_at보다 작고, end_at은 start_at보다 큰 경우는 포함시키지 못함
                # TODO: 영상 끝 시간 정보를 알 수 있는지 확인해야 됨.
                movie_match.append(key)

        return movie_match
