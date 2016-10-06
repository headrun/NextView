from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Center(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = u'center'
    def __unicode__(self):
        return self.name

class Project(models.Model):
    name    = models.CharField(max_length=255)
    code    = models.IntegerField(max_length=255, unique=True)
    center  = models.ForeignKey(Center, null=True)
    layout  = models.CharField(max_length=855, default='')
    project_db_handlings_choices = (('update','Update'),('aggregate','Aggregate'),('ignore','Ignore'),)
    project_db_handling = models.CharField(max_length=30,choices=project_db_handlings_choices,default='ignore',) 

    class Meta:
        db_table = u'project'
    def __unicode__(self):
        return self.name

class TeamLead(models.Model):
    name    = models.ForeignKey(User, null=True)
    center  = models.ForeignKey(Center, null=True)
    project = models.ForeignKey(Project, null=True)

    class Meta:
        db_table = u'agent'
    def __unicode__(self):
        user_obj = User.objects.filter(id=self.name_id).values_list('username',flat=True)
        return user_obj[0]

class Customer(models.Model):
    name    = models.ForeignKey(User, null=True)
    center  = models.ManyToManyField(Center, null=True)
    project = models.ManyToManyField(Project, null=True)

    class Meta:
        db_table = u'customer'
    def __unicode__(self):
        user_obj = User.objects.filter(id=self.name_id).values_list('username',flat=True)
        return user_obj[0]

class Centermanager(models.Model):
    name    = models.ForeignKey(User, null=True)
    center  = models.ForeignKey(Center, null=True)

    class Meta:
        db_table = u'center_manager'
    def __unicode__(self):
        user_obj = User.objects.filter(id=self.name_id).values_list('username',flat=True)
        return user_obj[0]

class Nextwealthmanager(models.Model):
    name    = models.ForeignKey(User, null=True)
    center  = models.ManyToManyField(Center)

    class Meta:
        db_table = u'nextwealthmanager'
    def __unicode__(self):
        user_obj = User.objects.filter(id=self.name_id).values_list('username',flat=True)
        return user_obj[0]

class RawTable(models.Model):
    team_lead   = models.ForeignKey(TeamLead, null=True)
    employee_id = models.CharField(max_length=255, blank=True)
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255)
    sub_packet  = models.CharField(max_length=255, blank=True)
    per_hour    = models.IntegerField(max_length=255, default=0)
    per_day     = models.IntegerField(max_length=255, default=0)
    date = models.DateField()
    norm        = models.IntegerField(max_length=255, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True,null=True)
    center      = models.ForeignKey(Center, null=True)
    project     = models.ForeignKey(Project, null=True)

    class Meta:
        db_table = u'raw_table'



class Internalerrors(models.Model):
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255)
    sub_packet = models.CharField(max_length=255, blank=True)
    error_name = models.CharField(max_length=255, blank=True)
    audited_errors = models.IntegerField(max_length=255,blank=True,default=0)
    total_errors = models.IntegerField(max_length=255,default=0,verbose_name='total_errors')
    date = models.DateField()
    employee_id = models.CharField(max_length=255,blank=True)
    center      = models.ForeignKey(Center, null=True)
    project     = models.ForeignKey(Project, null=True)

    class Meta:
        db_table = u'internal_error'
        #unique_together = ("audited_errors","error_value","date","employee_id","volume_type")

    def __unicode__(self):
        return self.employee_id


class Externalerrors(models.Model):
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255)
    sub_packet = models.CharField(max_length=255, blank=True)
    error_name = models.CharField(max_length=255, blank=True)
    audited_errors = models.IntegerField(max_length=255, blank=True, default=0)
    total_errors = models.IntegerField(max_length=255, default=0, verbose_name='total_errors')
    date = models.DateField()
    employee_id = models.CharField(max_length=255, blank=True)
    center = models.ForeignKey(Center, null=True)
    project = models.ForeignKey(Project, null=True)

    class Meta:
        db_table = u'external_error'
        #unique_together = ("audited_errors","error_value","date","employee_id","volume_type")

    def __unicode__(self):
        return self.employee_id


class Authoringtable(models.Model):
    project = models.ForeignKey(Project, null=True)
    sheet_name = models.CharField(max_length=255, default='')
    table_schema = models.CharField(max_length=255, default='')
    sheet_field = models.CharField(max_length=255, default='')
    center = models.ForeignKey(Center, null=True)
    table_type_choices = (('raw_table', 'Raw_table'), ('external_error', 'External_error'), ('internal_error', 'Internal_error'),('target', 'targets'), ('other', 'Other'),('internal_external','Error'))
    table_type = models.CharField(max_length=30, choices=table_type_choices, default='other', )


    class Meta:
        db_table = u'authoring_table'
    def __unicode__(self):
        return self.table_schema

class Document(models.Model):
    document = models.FileField(upload_to='media/preprocessing/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    #status = models.IntegerField(max_length=2, default=0)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = u'upload_table'

    def __unicode__(self):
        return self.description

class Targets(models.Model):
    from_date = models.DateField()
    to_date   = models.DateField()
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255)
    sub_packet  = models.CharField(max_length=255, blank=True)
    target      = models.IntegerField(max_length=125)
    center = models.ForeignKey(Center, null=True)
    project = models.ForeignKey(Project, null=True)

    class Meta:
        db_table = u'target_table'

    def __unicode__(self):
        return self.work_packet

class Worktrack(models.Model):
    date = models.DateField()
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255)
    sub_packet = models.CharField(max_length=255, blank=True)
    opening    = models.IntegerField(max_length=125)
    received   = models.IntegerField(max_length=125)
    non_workable_count = models.IntegerField(max_length=125,blank=True,default=0)
    completed   = models.IntegerField(max_length=125)
    closing_balance  = models.IntegerField(max_length=125)
    center = models.ForeignKey(Center, null=True)
    project = models.ForeignKey(Project, null=True)

    class Meta:
        db_table = u'worktrack_table'

    def __unicode__(self):
        return self.work_packet
