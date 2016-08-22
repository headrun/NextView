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
    center  = models.ForeignKey(Center, null=True)
    project = models.ForeignKey(Project, null=True)

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
    employee    = models.CharField(max_length=255, default='')
    volume_type = models.CharField(max_length=255, default='')
    per_hour    = models.IntegerField(max_length=255, default=0)
    per_day     = models.IntegerField(max_length=255, default=0)
    date        = models.DateTimeField()
    norm        = models.IntegerField(max_length=255, default=0)
    created_at  = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True,null=True)
    center      = models.ForeignKey(Center, null=True)
    project     = models.ForeignKey(Project, null=True)

    class Meta:
        db_table = u'raw_table'
        #unique_together = (("date","employee"),)

class Error(models.Model):
    volume_type = models.CharField(max_length=255, default='')
    #error_type = models.CharField(max_length=255, default='')
    audited_errors = models.IntegerField(max_length=255,default=0)
    error_value = models.IntegerField(max_length=255,default=0,verbose_name='total_errors')
    date = models.DateField()
    employee_id = models.CharField(max_length=255,default='')

    class Meta:
        db_table = u'api_error'
        #db_table = u'api_error'
        #unique_together = (("audited_errors","error_value"),)

    def __unicode__(self):
        return self.employee_id
<<<<<<< HEAD
=======

>>>>>>> 1b1be63c830ca57877d92bdc71c58533eb590e81

class Externalerrors(models.Model):
    volume_type = models.CharField(max_length=255, default='')
    error_type = models.CharField(max_length=255, default='')
    error_value = models.IntegerField(max_length=255, default=0)
    date = models.DateField()
    employee_id = models.CharField(max_length=255, default='')
<<<<<<< HEAD
=======
    agent_reply = models.CharField(max_length=255, default='')
>>>>>>> 1b1be63c830ca57877d92bdc71c58533eb590e81

    class Meta:
        db_table = u'external_errors'
        #unique_together = (("error_type", "error_value"),)

    def __unicode__(self):
        return self.employee_id

<<<<<<< HEAD
=======

>>>>>>> 1b1be63c830ca57877d92bdc71c58533eb590e81
class Authoringtable(models.Model):
    project = models.ForeignKey(Project, null=True)
    sheet_name = models.CharField(max_length=255, default='')
    table_schema = models.CharField(max_length=255, default='')
    sheet_field = models.CharField(max_length=255, default='')

    class Meta:
        db_table = u'authoring_table'
    def __unicode__(self):
<<<<<<< HEAD
        return self.table_schema
=======
        return self.table_schema
>>>>>>> 1b1be63c830ca57877d92bdc71c58533eb590e81
