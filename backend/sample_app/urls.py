from django.urls import path

from .api_test import task, movie, sensor, eventmemo
from . import api
from . import api_class

app_name = 'sample_app'

urlpatterns = [
    # path('', api_test.index, name='index'),
    path('task/', api.task),
    path('task/<int:task_id>/', api.to_taskpage),
    path('movie/', api.handle_movie_info),
    path('movie/<int:movie_id>/', api.label_movie),
    # path('timerange/', api.check_timerange),
    path('task/<int:task_id>/movie/', api.get_movie),
    path('task/<int:task_id>/trajectory/', api.get_trajectory),
    path('task/<int:task_id>/sensor-imu/', api.get_sensor_imu),
    path('task/<int:task_id>/event-timeline/', api.handle_event_timeline),
    path('test_task/', task.Task.as_view()),
    path('test_task/<int:task_id>/', task.ToTaskPage.as_view()),
    path('test_task/<int:task_id>/movie/', movie.Movie.as_view()),
    path('test_task/<int:task_id>/trajectory/', sensor.Trajectory.as_view()),
    path('test_task/<int:task_id>/sensor-imu/', sensor.SensorIMU.as_view()),
    path('test_task/<int:task_id>/event-timeline/', eventmemo.EventMemo.as_view()),
]