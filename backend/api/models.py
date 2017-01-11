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
    #code    = models.IntegerField(max_length=255, unique=True)
    center  = models.ForeignKey(Center, null=True)
    #layout  = models.CharField(max_length=512, default='')
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

class ChartType(models.Model):
    chart_type = models.CharField(max_length=512)

    class Meta:
        db_table = u'chart_type'

    def __unicode__(self):
        return self.chart_type

class Customer(models.Model):
    name    = models.ForeignKey(User, null=True)
    center  = models.ManyToManyField(Center, null=True)
    project = models.ManyToManyField(Project, null=True)
    #layout = models.CharField(max_length=512, default='')
    is_drilldown = models.BooleanField(default=None)

    class Meta:
        db_table = u'customer'
    def __unicode__(self):
        user_obj = User.objects.filter(id=self.name_id).values_list('username',flat=True)
        return user_obj[0]

class Widgets(models.Model):
    config_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    col = models.IntegerField(max_length=125)
    api = models.CharField(max_length=255,null=True, blank=True)
    opt = models.CharField(max_length=225)
    id_num = models.IntegerField(max_length=125)
    day_type_widget = models.BooleanField(default=None)
    priority = models.IntegerField(max_length=125,null=True, blank=True)
    chart_type_name = models.ForeignKey(ChartType, null=True)

    class Meta:
        db_table = u'widgets'
    def __unicode__(self):
        return self.name

class Widget_Mapping(models.Model):
    user_name = models.ForeignKey(User, null=True)
    widget_name = models.ForeignKey(Widgets, null=True)
    widget_priority = models.IntegerField(max_length=125)
    is_display = models.BooleanField(default=None)
    is_drilldown = models.BooleanField(default=None)

    class Meta:
        db_table = u'widget_mapping'
    def __unicode__(self):
        return u''
class Headcount(models.Model):
    #from_date = models.DateField()
    date   = models.DateField()
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255,blank=True)
    sub_packet = models.CharField(max_length=255, blank=True)
    center = models.ForeignKey(Center, null=True)
    project = models.ForeignKey(Project, null=True)
    billable_agent = models.IntegerField(max_length=125)
    buffer_agent = models.IntegerField(max_length=125)
    billable_support = models.IntegerField(max_length=125)
    buffer_support = models.IntegerField(max_length=125)
    non_billable_support_others = models.IntegerField(max_length=125)
    support_others_managers = models.IntegerField(max_length=125)
    total = models.IntegerField(max_length=125,default = "")

    class Meta:
        db_table = u'headcount_table'

    def __unicode__(self):
        return self.work_packet

class HeadcountAuthoring(models.Model):
    date = models.CharField(max_length=255)
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255, blank=True)
    sub_packet = models.CharField(max_length=255, blank=True)
    center = models.ForeignKey(Center, null=True)
    project = models.ForeignKey(Project, null=True)
    billable_agent = models.CharField(max_length=255)
    buffer_agent = models.CharField(max_length=255, blank=True)
    billable_support = models.CharField(max_length=255, blank=True)
    buffer_support = models.CharField(max_length=255, blank=True)
    non_billable_support_others = models.CharField(max_length=255, blank=True)
    support_others_managers = models.CharField(max_length=255, blank=True)
    total = models.CharField(max_length=125, blank=True)
    sheet_name = models.CharField(max_length=255, default='')

    class Meta:
        db_table = u'headcount_authoring'
    def __unicode__(self):
        return self.work_packet



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


class RawtableAuthoring(models.Model):
    employee_id = models.CharField(max_length=255, blank=True)
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255)
    sub_packet  = models.CharField(max_length=255, blank=True)
    per_hour    = models.CharField(max_length=255, blank=True)
    per_day     = models.CharField(max_length=255, blank=True)
    date = models.CharField(max_length=255)
    norm        = models.CharField(max_length=255, blank=True)
    center      = models.ForeignKey(Center, null=True)
    project     = models.ForeignKey(Project, null=True)
    sheet_name = models.CharField(max_length=255, default='')
    ignorable_fileds = models.CharField(max_length=255, blank=True,default='')

    class Meta:
        db_table = u'rawtable_authoring'
    
    def __unicode__(self):
        return self.work_packet





class Internalerrors(models.Model):
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255)
    sub_packet = models.CharField(max_length=255, blank=True)
    #error_name = models.CharField(max_length=255, blank=True)
    error_types = models.CharField(max_length=512, blank=True)
    error_values = models.CharField(max_length=512, blank=True)
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


class InternalerrorsAuthoring(models.Model):
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255)
    sub_packet = models.CharField(max_length=255, blank=True)
    #error_name = models.CharField(max_length=255, blank=True)
    #error_type1 = models.CharField(max_length=255, blank=True)
    #error_type2 = models.CharField(max_length=255, blank=True)
    #error_type3 = models.CharField(max_length=255, blank=True)
    #error_type4 = models.CharField(max_length=255, blank=True)
    #error_type5 = models.CharField(max_length=255, blank=True)
    #error_type6 = models.CharField(max_length=255, blank=True)
    #error_type7 = models.CharField(max_length=255, blank=True)
    #error_type8 = models.CharField(max_length=255, blank=True)
    #error_type9 = models.CharField(max_length=255, blank=True)
    audited_errors = models.CharField(max_length=255,blank=True,verbose_name='Audited_errors')
    total_errors = models.CharField(max_length=255,default=0,verbose_name='total_errors')
    error_category = models.CharField(max_length=255, blank=True)
    error_count = models.CharField(max_length=255, blank=True)
    date = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=255,blank=True)
    center      = models.ForeignKey(Center, null=True)
    project     = models.ForeignKey(Project, null=True)
    sheet_name = models.CharField(max_length=255, default='')

    class Meta:
        db_table = u'internalerrors_authoring'
        #unique_together = ("audited_errors","error_value","date","employee_id","volume_type")

    def __unicode__(self):
        return self.work_packet

class Externalerrors(models.Model):
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255)
    sub_packet = models.CharField(max_length=255, blank=True)
    #error_name = models.CharField(max_length=255, blank=True)
    error_types = models.CharField(max_length=512, blank=True)
    error_values = models.CharField(max_length=512, blank=True)
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


class ExternalerrorsAuthoring(models.Model):
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255)
    sub_packet = models.CharField(max_length=255, blank=True)
    #error_name = models.CharField(max_length=255, blank=True)
    #error_type1 = models.CharField(max_length=255, blank=True)
    #error_type2 = models.CharField(max_length=255, blank=True)
    #error_type3 = models.CharField(max_length=255, blank=True)
    #error_type4 = models.CharField(max_length=255, blank=True)
    #error_type5 = models.CharField(max_length=255, blank=True)
    #error_type6 = models.CharField(max_length=255, blank=True)
    #error_type7 = models.CharField(max_length=255, blank=True)
    #error_type8 = models.CharField(max_length=255, blank=True)
    #error_type9 = models.CharField(max_length=255, blank=True)
    audited_errors = models.CharField(max_length=255,blank=True,verbose_name='Audited_errors')
    total_errors = models.CharField(max_length=255,default=0,verbose_name='total_errors')
    error_category = models.CharField(max_length=255, blank=True)
    error_count = models.CharField(max_length=255, blank=True)
    date = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=255,blank=True)
    center      = models.ForeignKey(Center, null=True)
    project     = models.ForeignKey(Project, null=True)
    sheet_name = models.CharField(max_length=255, default='')

    class Meta:
        db_table = u'externalerrors_authoring'
        #unique_together = ("audited_errors","error_value","date","employee_id","volume_type")

    def __unicode__(self):
        return self.work_packet


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
    fte_target  = models.IntegerField(max_length=125,default=0)
    center = models.ForeignKey(Center, null=True)
    project = models.ForeignKey(Project, null=True)

    class Meta:
        db_table = u'target_table'

    def __unicode__(self):
        return self.work_packet

class TargetsAuthoring(models.Model):
    from_date = models.CharField(max_length=255)
    to_date   = models.CharField(max_length=255)
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255)
    sub_packet  = models.CharField(max_length=255, blank=True)
    target      = models.CharField(max_length=125)
    fte_target = models.CharField(max_length=125, blank=True)
    center = models.ForeignKey(Center, null=True)
    project = models.ForeignKey(Project, null=True)
    sheet_name = models.CharField(max_length=255, default='')
    class Meta:
        db_table = u'targets_authoring'

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

class WorktrackAuthoring(models.Model):
    date = models.CharField(max_length=255, blank=True)
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255)
    sub_packet = models.CharField(max_length=255, blank=True)
    opening    = models.CharField(max_length=125)
    received   = models.CharField(max_length=125)
    non_workable_count = models.CharField(max_length=125,blank=True)
    completed   = models.CharField(max_length=125)
    closing_balance  = models.CharField(max_length=125)
    center = models.ForeignKey(Center, null=True)
    project = models.ForeignKey(Project, null=True)
    sheet_name = models.CharField(max_length=255, default='')

    class Meta:
        db_table = u'worktrack_authornig'

    def __unicode__(self):
        return self.work_packet

class Color_Mapping(models.Model):
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255, blank=True)
    sub_packet = models.CharField(max_length=255, blank=True)
    color_code = models.CharField(max_length=255)
    center = models.ForeignKey(Center, null=True)
    project = models.ForeignKey(Project, null=True)
    class Meta:
        db_table = u'color_mappping'

    def __unicode__(self):
        return self.work_packet

class Annotation(models.Model):
    epoch = models.CharField(max_length=40,verbose_name='selected_date')
    text = models.TextField()
    key = models.CharField(max_length=512, null=True)
    #widget_name = models.ForeignKey(Widgets)
    dt_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    center = models.ForeignKey(Center)
    project = models.ForeignKey(Project)
    chart_type_name = models.ForeignKey(ChartType, null=True)

    class Meta:
        db_table = u'annotations'

    def __unicode__(self):
        return self.epoch
