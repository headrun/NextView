from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User, Group


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
    layout  = models.CharField(max_length=512, default='')
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
    layout = models.CharField(max_length=512, default='')
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

    class Meta:
        db_table = u'widgets'
    def __unicode__(self):
        return self.name

'''class Widget_Mapping(models.Model):
    user_name = models.ForeignKey(User, null=True)
    widget_name = models.ForeignKey(Widgets, null=True)
    widget_priority = models.IntegerField(max_length=125)
    is_display = models.BooleanField(default=None)
    is_drilldown = models.BooleanField(default=None)

    class Meta:
        db_table = u'widget_mapping'
    def __unicode__(self):
        return u'' '''

class Widgets_group(models.Model):
    User_Group = models.ForeignKey(Group)
    project = models.ForeignKey(Project, null=True)
    center = models.ForeignKey(Center, null=True)
    widget_name = models.ForeignKey(Widgets, null=True)
    widget_priority = models.IntegerField(max_length=125)
    is_display = models.BooleanField(default=None)
    is_drilldown = models.BooleanField(default=None)

    class Meta:
        db_table = u'Widgets_group'
    def __unicode__(self):
        return u''

class Headcount(models.Model):
    date = models.DateField()
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255)
    sub_packet = models.CharField(max_length=255, blank=True)
    center = models.ForeignKey(Center, null=True)
    project = models.ForeignKey(Project, null=True)
    billable_agent = models.FloatField(max_length=125, default=0)
    buffer_agent = models.FloatField(max_length=125, default=0)
    billable_support = models.FloatField(max_length=125, default=0)
    buffer_support = models.FloatField(max_length=125, default=0)
    non_billable_support_others = models.FloatField(max_length=125, default=0)
    support_others_managers = models.FloatField(max_length=125, default=0)
    total = models.FloatField(max_length=125, default=0)

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
    audited_errors = models.CharField(max_length=255,blank=True,verbose_name='Audited_errors')
    total_errors = models.CharField(max_length=255,default=0,verbose_name='total_errors')
    error_category = models.CharField(max_length=255, blank=True)
    error_count = models.CharField(max_length=255, blank=True)
    date = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=255,blank=True)
    center      = models.ForeignKey(Center, null=True)
    project     = models.ForeignKey(Project, null=True)
    sheet_name = models.CharField(max_length=255, default='')
    total_errors_require = models.BooleanField(default=None)

    class Meta:
        db_table = u'internalerrors_authoring'

    def __unicode__(self):
        return self.work_packet

class Externalerrors(models.Model):
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255)
    sub_packet = models.CharField(max_length=255, blank=True)
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

    def __unicode__(self):
        return self.employee_id


class ExternalerrorsAuthoring(models.Model):
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255)
    sub_packet = models.CharField(max_length=255, blank=True)
    audited_errors = models.CharField(max_length=255,blank=True,verbose_name='Audited_errors')
    total_errors = models.CharField(max_length=255,default=0,verbose_name='total_errors')
    error_category = models.CharField(max_length=255, blank=True)
    error_count = models.CharField(max_length=255, blank=True)
    date = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=255,blank=True)
    center      = models.ForeignKey(Center, null=True)
    project     = models.ForeignKey(Project, null=True)
    sheet_name = models.CharField(max_length=255, default='')
    total_errors_require = models.BooleanField(default=None)
    class Meta:
        db_table = u'externalerrors_authoring'

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
    fte_target = models.CharField(max_length=125, default=0)
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
    work_packet = models.CharField(max_length=255,blank=True)
    sub_packet = models.CharField(max_length=255, blank=True)
    color_code = models.CharField(max_length=255)
    center = models.ForeignKey(Center, null=True)
    project = models.ForeignKey(Project, null=True)
    class Meta:
        db_table = u'color_mappping'

    def __unicode__(self):
        return self.work_packet


class Alias_Widget(models.Model):
    center = models.ForeignKey(Center, null=True)
    project = models.ForeignKey(Project, null=True)
    widget_name = models.ForeignKey(Widgets, null=True)
    alias_widget_name = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'alias_widget'

    def __unicode__(self):
        return '%s %s' % (str(self.widget_name), str(self.project))
        #return str(self.widget_name)

class Alias_packets(models.Model):
    #widget = models.ForeignKey(Alias_Widget, related_name="widget_name",null=True)
    widget = models.ForeignKey(Alias_Widget, null=True)
    existed_name = models.CharField(max_length=255, blank=True)
    alias_name = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'alias_packets'

    def __unicode__(self):
        return self.alias_name

class TatAuthoring(models.Model):
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255, blank=True)
    sub_packet = models.CharField(max_length=255, blank=True)
    center = models.ForeignKey(Center, null=True)
    project = models.ForeignKey(Project, null=True)
    received_date = models.CharField(max_length=255, blank=True)
    total_received = models.CharField(max_length=255, blank=True)
    scan_date = models.CharField(max_length=255, blank=True)
    completed_date = models.CharField(max_length=255, blank=True)
    met_count = models.CharField(max_length=125, blank = True)
    non_met_count = models.CharField(max_length=125, blank= True)
    tat_status = models.CharField(max_length=255, blank=True)
    sheet_name = models.CharField(max_length=255, default='')

    class Meta:
        db_table = u'tat_authoring'

    def __unicode__(self):
        return self.tat_status

class TatTable(models.Model):
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255)
    sub_packet = models.CharField(max_length=255, blank=True)
    center = models.ForeignKey(Center, null=True)
    project = models.ForeignKey(Project, null=True)
    date = models.DateField()
    completed_date = models.DateField(null=True)
    scan_date = models.DateField(null=True)
    total_received = models.IntegerField(max_length=255)
    met_count = models.IntegerField(max_length=125)
    non_met_count = models.IntegerField(max_length=125, blank= True)
    tat_status = models.CharField(max_length=255)

    class Meta:
        db_table = u'tats_table'

    def __unicode__(self):
        return self.tat_status

'''class StatusTable(models.Model):
    sub_project = models.CharField(max_length=255, blank=True)
    work_packet = models.CharField(max_length=255, blank=True)
    sub_packet = models.CharField(max_length=255, blank=True)
    center = models.ForeignKey(Center, null=True)
    project = models.ForeignKey(Project, null=True)
    received_date = models.DateField()
    completed_date = models.DateField()
    scan_date = models.DateField()
    total_received = models.IntegerField(max_length=255, blank=True)
    met_count = models.IntegerField(max_length=125, blank = True)
    non_met_count = models.IntegerField(max_length=125, blank= True)
    tat_status = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = u'status_table'

    def __unicode__(self):
        return self.met_count'''