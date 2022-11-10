from library.postgresql_libs import PostgreSQL
from create_table_in_postgresql import create_table

post = PostgreSQL()

first_table_insert = {
    'car_class': {
        'col': ['car_class_name', 'car_manufacturer'],
        'data': [
            ['M5 E39 5.0', 'BMW'],
            ['BT44B', 'BRABHAM'],
            ['GT-R GT500 2013', 'NISSAN'],
            ['CLIO CUP 200 TURBO', 'RENAULT'],
            ['STOCKCAR 2018 CUP', 'EDGAR GT'],
            ['STOCKCAR 2018 CUP', 'CENTENNIAL'],
            ['ADAC LUPO CUP 2003', 'VOLKSWAGEN'],
            ['LUPO GTI 2003', 'VOLKSWAGEN'],
            ['aDRT', '42dot'],
            ['TSD-A01', '42dot'],
        ]
    },

    'blackbox_device': {
        'col': ['blackbox_model_id', 'blackbox_device_serial_number', 'blackbox_last_checked_at', 'blackbox_firmware_version', 'blackbox_firmware_updated_at'],
        'data': [
            [1, 123456789, '2022-01-01 KST', '{0, 0, 1}', '2022-01-01 KST'],
            [2, 123456789, '2022-10-01 KST', '{0, 0, 2}', '2022-10-12 KST'],
        ]
    },

    'driver': {
        'col': ['driver_name', 'driver_gender', 'driver_created_at', 'driver_birthday'],
        'data': [
            ['suhyun.kim', True, '2022-01-01', '1998-05-07'],
            ['chulsu.ha', True, '2022-01-01', '1988-02-13'],
            ['seungeun.kang', True, '2022-01-01', '1996-11-02']
        ]
    },

    'manager': {
        'col': ['manager_name', 'manager_role'],
        'data': [
            ['suhyun.kim', 1],
            ['seungeun.kang', 1],
            ['chulsu.ha', 1],
            ['test_model_1', 2]
        ]
    }
}

second_table_insert = {
    'car': {
        'col': ['car_class_id', 'car_num', 'blackbox_device_id'],
        'data': [
            [1, '001허0001', 1],
            [8, '001허0002', 1]
        ]
    },

    'accident_detection_model': {
        'col': ['manager_id', 'accident_model_name', 'accident_model_version', 'train_set', 'test_set', 'tp', 'fp', 'fn', 'tn'],
        'data': [
            [4, 'geotab_rulebase', '{0, 0, 1}', 'N/A', 'N/A', 56, 6, 0, 0]
        ]
    },

    'blackbox_movie': {
        'col': ['blackbox_movie_name', 'car_id', 'blackbox_device_id', 'movie_upload_at', 'movie_start_at', 'movie_end_at'],
        'data': [
            ['20220907_120000_normal_1.mp4', 1, 1, '2022-09-07 12:10:00 UTC', '2022-09-07 12:00:00 UTC', '2022-09-07 12:01:00 UTC'],
            ['20220907_120100_normal_1.mp4', 1, 1, '2022-09-07 12:11:00 UTC', '2022-09-07 12:01:00 UTC', '2022-09-07 12:02:00 UTC'],
            ['20220907_120200_normal_1.mp4', 1, 1, '2022-09-07 12:12:00 UTC', '2022-09-07 12:02:00 UTC', '2022-09-07 12:03:00 UTC'],
            ['20220907_120300_normal_1.mp4', 1, 1, '2022-09-07 12:13:00 UTC', '2022-09-07 12:03:00 UTC', '2022-09-07 12:04:00 UTC'],
            ['20220907_120400_normal_1.mp4', 1, 1, '2022-09-07 12:14:00 UTC', '2022-09-07 12:04:00 UTC', '2022-09-07 12:05:00 UTC'],
            ['20220907_120500_normal_1.mp4', 1, 1, '2022-09-07 12:15:00 UTC', '2022-09-07 12:05:00 UTC', '2022-09-07 12:06:00 UTC'],
            ['20220907_120600_normal_1.mp4', 1, 1, '2022-09-07 12:16:00 UTC', '2022-09-07 12:06:00 UTC', '2022-09-07 12:07:00 UTC']
        ]
    }
}

# sensor data 임시로 만들기


temp_sensor_data_timestamp = ', '.join([f'2022-09-21 15:38:{26+i} KST' for i in range(10)])
temp_sensor_data_timestamp = "'{" + temp_sensor_data_timestamp + "}'::timestamp[]"
acc_x = '{0.1, 0.1, 0.1, 0.1, 0.1, 38.9, 23.1, 24.1, 4.2, 0.3}'
acc_y = '{0.1, 0.1, 0.1, 0.1, 0.1, 38.9, 32.6, 42.1, 4.2, 0.3}'
acc_z = '{0.1, 0.1, 0.1, 0.1, 0.1, 38.9, 23.1, 10.1, 4.2, 0.3}'

temp_sensor_data_timestamp2 = ', '.join([f'2022-09-21 15:23:{12+i} KST' for i in range(10)])
temp_sensor_data_timestamp2 = "'{" + temp_sensor_data_timestamp2 + "}'::timestamp[]"
acc_x2 = '{0.1, 17.1, 0.1, 0.1, 0.1, 38.9, 23.1, 24.1, 4.2, 0.3}'
acc_y2 = '{0.1, 16.1, 0.1, 0.1, 0.1, 38.9, 32.6, 42.1, 4.2, 0.3}'
acc_z2 = '{0.1, 38.1, 0.1, 0.1, 0.1, 38.9, 23.1, 10.1, 4.2, 0.3}'


third_table_insert = {
    'sensor_data': {
        'col': ['car_id', 'timestamp_ref', 'accident_model_id', 'acc_x', 'acc_y', 'acc_z'],
        'data': [
            [1, temp_sensor_data_timestamp, 1, acc_x, acc_y, acc_z],
            [1, temp_sensor_data_timestamp2, 1, acc_x2, acc_y2, acc_z2],
        ]
    },
    'accident_prediction_result': {
        'col': ['accident_model_id', 'sensor_data_set_id', 'accident_probability'],
        'data': [
            # string 합치는 방법으로 넣을 수 없음. '{2022-09-20, 2022-09-21}'::date[] 이런식으로 들어가야 하는데..
            [1, 1, '{14.1, 10.1, 13.2, 24.3, 13.8, 82.4, 81.9, 97.8, 32.2, 20.2}'],
            [1, 2, '{14.1, 57.1, 13.2, 24.3, 13.8, 82.4, 81.9, 97.8, 32.2, 20.2}'],
        ]
    },
    'accident_investigation_card': {
        'col': ['manager_id', 'car_id', 'driver_id', 'investigation_start_time', 'investigation_end_time', 'card_created_at', 'card_updated_at', 'work_done', 'card_made_by_id', 'memo', 'is_accident'],
        'data': [
            [3, 1, 3, '2022-09-21 15:35:00 KST', '2022-09-21 16:00:00 KST', '2022-09-22 09:37:00', '2022-09-22 09:37:00', True, 4, '사고카드 테스트 1', 82],
            [1, 2, 1, '2022-09-21 15:20:00 KST', '2022-09-21 15:50:00 KST', '2022-09-22 10:21:00', '2022-09-22 10:21:00', True, 4, '사고카드 테스트 2', 93]
        ]
    }
}

fourth_table_insert = {
    'event_timeline_memo': {
        'col': ['accident_investigation_card_id', 'car_id', 'event_at', 'event_desc', 'event_desc_created_at', 'event_desc_modified_at', 'is_valid', 'is_accident'],
        'data': [
            [1, 1, '2022-09-21 15:38:31 KST', '테스트: 졸음운전 같음', '2022-09-22 09:38:00 KST', '2022-09-22 09:38:00 KST', True, 0],
            [1, 1, '2022-09-21 15:38:31 KST', '테스트: 사고발생1', '2022-09-22 09:38:00 KST', '2022-09-22 09:38:00 KST', True, 1],
            [1, 1, '2022-09-21 15:38:32 KST', '테스트: 사고발생2', '2022-09-22 09:38:05 KST', '2022-09-22 09:38:05 KST', True, 1],
            [1, 1, '2022-09-21 15:38:33 KST', '테스트: 사고발생3', '2022-09-22 09:38:12 KST', '2022-09-22 09:38:12 KST', True, 1],
            [2, 2, '2022-09-21 15:23:13 KST', '테스트: 사고 애매함', '2022-09-22 10:22:00 KST', '2022-09-22 10:22:00 KST', True, -1],
            [2, 2, '2022-09-21 15:23:17 KST', '테스트: 사고발생2', '2022-09-22 10:22:20 KST', '2022-09-22 10:22:20 KST', True, 1],
            [2, 2, '2022-09-21 15:23:18 KST', '테스트: 사고발생3', '2022-09-22 10:22:34 KST', '2022-09-22 10:22:34 KST', True, 1],
            [2, 2, '2022-09-21 15:23:19 KST', '테스트: 사고발생4', '2022-09-22 10:22:58 KST', '2022-09-23 14:52:43 KST', True, 1]
        ]
    },

    'blackbox_movie_label_info': {
        'col': ['blackbox_movie_id', 'labeler_id', 'is_accident'],
        'data': [
            [1, 3, 1],
            [2, 1, -1]
        ]
    }
}


# serial number 초기화 하고 시작
def delete_table():
    table_name = [
        'driver',
        'car_class',
        'blackbox_device',
        'manager',
        'blackbox_movie',
        'car',
        'sensor_data',
        'accident_detection_model',
        'accident_prediction_result',
        'accident_investigation_card',
        'event_timeline_memo',
        'blackbox_movie_label_info'
    ]

    for t in table_name:
        query = f"""DROP table umos_fii.{t} CASCADE;"""
        post.cursor.execute(query)
        post.commit()


def reset_table():
    delete_table()
    create_table()


def insert_data():
    schema = 'umos_fii'
    for table_list in [first_table_insert, second_table_insert, third_table_insert, fourth_table_insert]:
        for table, data_dict in table_list.items():
            for v in data_dict['data']:
                post.insert(schema, table, data_dict['col'], v, if_conflict_do_nothing=True)


# TODO: 나중에 시간 나면 임시 데이터 넣는 클래스 짜서 더 쉽게 만들기

def insert_sample_data():
    schema = 'umos_fii'
    data = {
        'blackbox_movie': {
            'col': ['blackbox_movie_name', 'car_id', 'blackbox_device_id', 'movie_upload_at', 'movie_start_at',
                    'movie_end_at'],
            'data': [
                ['20220907_120000_normal_1.mp4', 1, 1, '2022-09-07 12:10:00 UTC', '2022-09-07 12:00:00 UTC',
                 '2022-09-07 12:01:00 UTC'],
                ['20220907_120100_normal_1.mp4', 1, 1, '2022-09-07 12:11:00 UTC', '2022-09-07 12:01:00 UTC',
                 '2022-09-07 12:02:00 UTC'],
                ['20220907_120200_normal_1.mp4', 1, 1, '2022-09-07 12:12:00 UTC', '2022-09-07 12:02:00 UTC',
                 '2022-09-07 12:03:00 UTC'],
                ['20220907_120300_normal_1.mp4', 1, 1, '2022-09-07 12:13:00 UTC', '2022-09-07 12:03:00 UTC',
                 '2022-09-07 12:04:00 UTC'],
                ['20220907_120400_normal_1.mp4', 1, 1, '2022-09-07 12:14:00 UTC', '2022-09-07 12:04:00 UTC',
                 '2022-09-07 12:05:00 UTC'],
                ['20220907_120500_normal_1.mp4', 1, 1, '2022-09-07 12:15:00 UTC', '2022-09-07 12:05:00 UTC',
                 '2022-09-07 12:06:00 UTC'],
                ['20220907_120600_normal_1.mp4', 1, 1, '2022-09-07 12:16:00 UTC', '2022-09-07 12:06:00 UTC',
                 '2022-09-07 12:07:00 UTC']
            ]
        }
    }
    for table, data_dict in data.items():
        for v in data_dict['data']:
            post.insert(schema, table, data_dict['col'], v, if_conflict_do_nothing=True)



if __name__ == "__main__":
    # reset_table()
    # insert_data()
    insert_sample_data()
