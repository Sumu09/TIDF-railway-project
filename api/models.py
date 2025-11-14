# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models




class Casedetails(models.Model):
    si_no = models.AutoField(db_column='SI_No', primary_key=True)  # Field name made lowercase.
    station_code = models.ForeignKey('Station', models.DO_NOTHING, db_column='Station_Code', to_field='station_code', blank=True, null=True)  # Correct to_field
    case = models.ForeignKey('Report', models.DO_NOTHING, db_column='Case_ID', to_field='case_id', blank=True, null=True)  # Correct to_field
    case_remark = models.TextField(db_column='Case_Remark', blank=True, null=True)  # Field name made lowercase.
    close = models.IntegerField(db_column='Close', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'casedetails'


class FinalReport(models.Model):
    si_no = models.IntegerField(db_column='SI_No')  # Field name made lowercase.
    train_name = models.CharField(db_column='Train_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    report_id = models.CharField(db_column='Report_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    wagon_no = models.IntegerField(db_column='Wagon_No', blank=True, null=True)  # Field name made lowercase.
    coach_position = models.IntegerField(db_column='Coach_Position', blank=True, null=True)  # Field name made lowercase.
    door_no = models.IntegerField(db_column='Door_No', blank=True, null=True)  # Field name made lowercase.
    camera_no = models.IntegerField(db_column='Camera_No', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    time = models.TimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    report_remark = models.TextField(db_column='Report_Remark', blank=True, null=True)  # Field name made lowercase.
    station_code = models.CharField(db_column='Station_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    station_name = models.CharField(db_column='Station_Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    case_id = models.IntegerField(db_column='Case_ID', blank=True, null=True)  # Field name made lowercase.
    image_link = models.CharField(db_column='Image_Link', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ph_no = models.BigIntegerField(db_column='Ph_No', blank=True, null=True)  # Field name made lowercase.
    user_name = models.CharField(db_column='User_Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    user_age = models.IntegerField(db_column='User_Age', blank=True, null=True)  # Field name made lowercase.
    user_email = models.CharField(db_column='User_Email', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'final_report'


class Goodstrains(models.Model):
    sl_no = models.AutoField(db_column='Sl_No', primary_key=True)  # Field name made lowercase.
    train_name = models.CharField(db_column='Train_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    train_status = models.CharField(db_column='Train_Status', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'goodstrains'


class PendingCases(models.Model):
    train = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pending_cases'


class Report(models.Model):
    si_no = models.AutoField(db_column='SI_No', primary_key=True)  # Field name made lowercase.
    train_name = models.CharField(db_column='Train_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    report_id = models.CharField(db_column='Report_ID', unique=True, max_length=20, blank=True, null=True)  # Field name made lowercase.
    wagon_no = models.IntegerField(db_column='Wagon_No', blank=True, null=True)  # Field name made lowercase.
    coach_position = models.IntegerField(db_column='Coach_Position', blank=True, null=True)  # Field name made lowercase.
    door_no = models.IntegerField(db_column='Door_No', blank=True, null=True)  # Field name made lowercase.
    camera_no = models.IntegerField(db_column='Camera_No', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    time = models.TimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    report_remark = models.TextField(db_column='Report_Remark', blank=True, null=True)  # Field name made lowercase.
    station_code = models.ForeignKey('Station', models.DO_NOTHING, db_column='Station_Code', to_field='station_code', blank=True, null=True)  # Correct to_field
    case_id = models.IntegerField(db_column='Case_ID', unique=True, blank=True, null=True)  # Field name made lowercase.
    image_link = models.CharField(db_column='Image_Link', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ph_no = models.BigIntegerField(db_column='Ph_No', blank=True, null=True)  # Field name made lowercase.
    zone = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report'


class Signup(models.Model):
    si_no = models.AutoField(db_column='SI_No', primary_key=True)  # Field name made lowercase.
    ph_no = models.BigIntegerField(db_column='Ph_No', unique=True, blank=True, null=True)  # Field name made lowercase.
    station_code = models.ForeignKey('Station', models.DO_NOTHING, db_column='Station_Code', to_field='station_code', blank=True, null=True)  # Correct to_field
    type_of_user = models.CharField(db_column='Type_of_User', max_length=50, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=100, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'signup'


class Station(models.Model):
    si_no = models.AutoField(db_column='SI_No', primary_key=True)  # Field name made lowercase.
    station_name = models.CharField(db_column='Station_Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    station_code = models.CharField(db_column='Station_Code', unique=True, max_length=20, blank=True, null=True)  # Field name made lowercase.
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    zone = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'station'


class Userdetails(models.Model):
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    age = models.IntegerField(db_column='Age', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ph_no = models.ForeignKey(Signup, models.DO_NOTHING, db_column='Ph_No', to_field='ph_no', blank=True, null=True)  # Correct to_field

    class Meta:
        managed = False
        db_table = 'userdetails'
