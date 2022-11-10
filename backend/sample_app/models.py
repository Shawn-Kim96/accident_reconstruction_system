# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccidentDetectionModel(models.Model):
    accident_model_id = models.AutoField(primary_key=True)
    manager = models.ForeignKey('Manager', models.DO_NOTHING)
    accident_model_name = models.CharField(max_length=255)
    accident_model_version = models.TextField()  # This field type is a guess.
    train_set = models.CharField(max_length=255)
    test_set = models.CharField(max_length=255)
    tp = models.IntegerField()
    fp = models.IntegerField()
    fn = models.IntegerField()
    tn = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'accident_detection_model'


class AccidentInvestigationCard(models.Model):
    accident_investigation_card_id = models.AutoField(primary_key=True)
    manager_id = models.IntegerField(null=True)
    car = models.ForeignKey('Car', models.DO_NOTHING)
    driver = models.ForeignKey('Driver', models.DO_NOTHING)
    card_created_at = models.DateTimeField()
    card_updated_at = models.DateTimeField()
    investigation_start_time = models.DateTimeField()
    investigation_end_time = models.DateTimeField()
    work_done = models.BooleanField(blank=True, null=True)
    card_made_by = models.ForeignKey('Manager', models.DO_NOTHING)
    memo = models.TextField(blank=True, null=True)
    is_accident = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accident_investigation_card'


class AccidentPredictionResult(models.Model):
    accident_prediction_result_id = models.AutoField(primary_key=True)
    accident_model = models.ForeignKey('Manager', models.DO_NOTHING)
    sensor_data_set = models.ForeignKey('SensorData', models.DO_NOTHING)
    accident_probability = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'accident_prediction_result'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BlackboxDevice(models.Model):
    blackbox_device_id = models.AutoField(primary_key=True)
    blackbox_model_id = models.IntegerField()
    blackbox_device_serial_number = models.IntegerField()
    blackbox_last_checked_at = models.DateTimeField()
    blackbox_firmware_version = models.TextField()  # This field type is a guess.
    blackbox_firmware_updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'blackbox_device'


class BlackboxMovie(models.Model):
    blackbox_movie_id = models.AutoField(primary_key=True)
    blackbox_movie_name = models.CharField(max_length=255)
    car = models.ForeignKey('Car', models.DO_NOTHING)
    blackbox_device = models.ForeignKey(BlackboxDevice, models.DO_NOTHING)
    movie_upload_at = models.DateTimeField()
    movie_start_at = models.DateTimeField()
    movie_end_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'blackbox_movie'


class BlackboxMovieLabelInfo(models.Model):
    blackbox_movie_label_info_id = models.AutoField(primary_key=True)
    blackbox_movie = models.ForeignKey('BlackboxMovie', models.DO_NOTHING)
    labeler = models.ForeignKey('Manager', models.DO_NOTHING)
    is_accident = models.IntegerField(blank=True, null=True)
    label_created_at = models.DateTimeField()
    label_modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
            managed = False
            db_table = 'blackbox_movie_label_info'


class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    car_class = models.ForeignKey('CarClass', models.DO_NOTHING)
    car_num = models.CharField(max_length=255)
    blackbox_device = models.ForeignKey(BlackboxDevice, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'car'


class CarClass(models.Model):
    car_class_id = models.AutoField(primary_key=True)
    car_class_name = models.CharField(max_length=255)
    car_manufacturer = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'car_class'


class Device(models.Model):
    id = models.UUIDField(primary_key=True)
    device_type_id = models.UUIDField()
    uid = models.CharField(unique=True, max_length=100)
    state = models.CharField(max_length=100)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device'


class DeviceType(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_type'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Driver(models.Model):
    driver_id = models.AutoField(primary_key=True)
    driver_name = models.CharField(max_length=255)
    driver_gender = models.BooleanField()
    driver_created_at = models.DateTimeField()
    driver_birthday = models.DateField()

    class Meta:
        managed = False
        db_table = 'driver'


class EventTimelineMemo(models.Model):
    event_timeline_memo_id = models.AutoField(primary_key=True)
    accident_investigation_card = models.ForeignKey(AccidentInvestigationCard, models.DO_NOTHING, blank=True, null=True)
    car_id = models.IntegerField()
    event_at = models.DateTimeField()
    event_desc = models.TextField()
    event_desc_created_at = models.DateTimeField()
    event_desc_modified_at = models.DateTimeField(blank=True, null=True)
    is_valid = models.BooleanField()
    is_accident = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_timeline_memo'


class Manager(models.Model):
    manager_id = models.AutoField(primary_key=True)
    manager_name = models.CharField(max_length=255)
    manager_role = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'manager'


class SensorData(models.Model):
    sensor_data_id = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car, models.DO_NOTHING)
    timestamp_ref = models.TextField()  # This field type is a guess.
    accident_model = models.ForeignKey(AccidentDetectionModel, models.DO_NOTHING)
    acc_x = models.TextField()  # This field type is a guess.
    acc_y = models.TextField()  # This field type is a guess.
    acc_z = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'sensor_data'


class UfosDeviceSample(models.Model):
    id = models.IntegerField(primary_key=True)
    device_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'ufos_device_sample'


class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True)
    vin = models.CharField(max_length=100)
    car_number = models.CharField(max_length=100)
    vehicle_class_id = models.UUIDField()
    status = models.CharField(max_length=100, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'vehicle'


class VehicleClass(models.Model):
    id = models.UUIDField(primary_key=True)
    brand_name = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_class'
