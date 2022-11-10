import psycopg2

from library.postgresql_libs import PostgreSQL

post = PostgreSQL()

create_table_commands_first = [
    """
    CREATE TABLE IF NOT EXISTS umos_fii.driver (
        driver_id SERIAL PRIMARY KEY,
        driver_name VARCHAR(255) NOT NULL,
        driver_gender BOOLEAN NOT NULL,
        driver_created_at TIMESTAMP with time zone NOT NULL,
        driver_birthday DATE NOT NULL
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS umos_fii.car_class (
        car_class_id SERIAL PRIMARY KEY,
        car_class_name VARCHAR(255) NOT NULL,
        car_manufacturer VARCHAR(255) NOT NULL
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS umos_fii.blackbox_device (
        blackbox_device_id SERIAL PRIMARY KEY,
        blackbox_model_id INT NOT NULL,
        blackbox_device_serial_number INT NOT NULL,
        blackbox_last_checked_at TIMESTAMP with time zone NOT NULL,
        blackbox_firmware_version INT[] NOT NULL,
        blackbox_firmware_updated_at TIMESTAMP with time zone NOT NULL
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS umos_fii.manager (
        manager_id SERIAL PRIMARY KEY,
        manager_name VARCHAR(255) NOT NULL,
        manager_role INT NOT NULL
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS umos_fii.accident_detection_model (
        accident_model_id SERIAL PRIMARY KEY,
        manager_id INTEGER NOT NULL REFERENCES umos_fii.manager (manager_id),
        accident_model_name VARCHAR(255) NOT NULL,
        accident_model_version INT[] NOT NULL,
        train_set VARCHAR(255) NOT NULL,
        test_set VARCHAR(255) NOT NULL,
        tp INTEGER NOT NULL,
        fp INTEGER NOT NULL,
        fn INTEGER NOT NULL,
        tn INTEGER NOT NULL
    )
    """
]

create_table_commands_second = [
    """
    CREATE TABLE IF NOT EXISTS umos_fii.car (
        car_id SERIAL PRIMARY KEY,
        car_class_id INTEGER NOT NULL REFERENCES umos_fii.car_class (car_class_id),
        car_num VARCHAR(255) NOT NULL,
        blackbox_device_id INTEGER NOT NULL REFERENCES umos_fii.blackbox_device (blackbox_device_id)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS umos_fii.blackbox_movie (
        blackbox_movie_id SERIAL PRIMARY KEY,
        blackbox_movie_name VARCHAR(255) NOT NULL,
        car_id INTEGER NOT NULL REFERENCES umos_fii.car (car_id),
        blackbox_device_id INTEGER NOT NULL REFERENCES umos_fii.blackbox_device (blackbox_device_id),
        movie_upload_at TIMESTAMP with time zone NOT NULL,
        movie_start_at TIMESTAMP with time zone NOT NULL,
        movie_end_at TIMESTAMP with time zone NOT NULL
    )
    """
]

create_table_commands_third = [
    """
    CREATE TABLE IF NOT EXISTS umos_fii.sensor_data (
        sensor_data_id SERIAL PRIMARY KEY,
        car_id INTEGER NOT NULL REFERENCES umos_fii.car (car_id),
        timestamp_ref TIMESTAMP with time zone[] NOT NULL,
        accident_model_id INT NOT NULL REFERENCES umos_fii.accident_detection_model,
        acc_x NUMERIC[] NOT NULL,
        acc_y NUMERIC[] NOT NULL,
        acc_z NUMERIC[] NOT NULL
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS umos_fii.accident_investigation_card (
        accident_investigation_card_id SERIAL PRIMARY KEY,
        manager_id INTEGER,
        car_id INTEGER NOT NULL REFERENCES umos_fii.car (car_id),
        driver_id INTEGER NOT NULL REFERENCES umos_fii.driver (driver_id),
        card_created_at TIMESTAMP with time zone NOT NULL,
        card_updated_at TIMESTAMP with time zone NOT NULL,
        investigation_start_time TIMESTAMP with time zone NOT NULL,
        investigation_end_time TIMESTAMP with time zone NOT NULL,
        work_done BOOLEAN,
        card_made_by_id INTEGER NOT NULL REFERENCES umos_fii.manager (manager_id),
        memo TEXT,
        is_accident INTEGER
    )
    """
]

create_table_commands_forth = [
    """
    CREATE TABLE IF NOT EXISTS umos_fii.accident_prediction_result (
        accident_prediction_result_id SERIAL PRIMARY KEY, 
        accident_model_id INTEGER NOT NULL REFERENCES umos_fii.manager (manager_id),
        sensor_data_set_id INTEGER NOT NULL REFERENCES umos_fii.sensor_data (sensor_data_id),
        accident_probability FLOAT[] NOT NULL
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS umos_fii.event_timeline_memo (
        event_timeline_memo_id SERIAL PRIMARY KEY,
        accident_investigation_card_id INTEGER REFERENCES umos_fii.accident_investigation_card (accident_investigation_card_id), 
        car_id INTEGER NOT NULL,
        event_at TIMESTAMP with time zone NOT NULL,
        event_desc TEXT NOT NULL,
        event_desc_created_at TIMESTAMP with time zone NOT NULL,
        event_desc_modified_at TIMESTAMP with time zone,
        is_valid BOOLEAN NOT NULL,
        is_accident INTEGER
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS umos_fii.blackbox_movie_label_info (
        blackbox_movie_label_info_id SERIAL PRIMARY KEY,
        blackbox_movie_id INTEGER NOT NULL REFERENCES umos_fii.blackbox_movie (blackbox_movie_id),
        labeler_id INTEGER NOT NULL REFERENCES umos_fii.manager (manager_id),
        is_accident INTEGER,
        label_created_at TIMESTAMP with time zone NOT NULL,
        label_modified_at TIMESTAMP with time zone
    )
    """
]


def create_table():
    for command_list in [
        create_table_commands_first,
        create_table_commands_second,
        create_table_commands_third,
        create_table_commands_forth
    ]:
        for command in command_list:
            try:
                post.cursor.execute(command)
                post.commit()
            except (Exception, psycopg2.DatabaseError) as e:
                print(e)


if __name__ == "__main__":
    create_table()
