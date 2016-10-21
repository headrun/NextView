from django.contrib import admin
# Register your models here.
from .models import *

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Project,ProjectAdmin)

class CenterAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Center,CenterAdmin)

class TeamleadAdmin(admin.ModelAdmin):
    list_display = ['name','project','center']
    list_filter = ('project','center')
admin.site.register(TeamLead,TeamleadAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Customer,CustomerAdmin)

class HeadcountAdmin(admin.ModelAdmin):
    list_display = ['work_packet','sub_packet','from_date','to_date','billable_agent']
admin.site.register(Headcount,HeadcountAdmin)

class CentermanagerAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Centermanager,CentermanagerAdmin)

class NextwealthmanagerAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Nextwealthmanager,NextwealthmanagerAdmin)

class RawtableAdmin(admin.ModelAdmin):
    list_display = ['work_packet','sub_project','sub_packet','per_day','employee_id','norm','date','created_at','modified_at']
    list_filter = ('work_packet', 'date','project','center')
admin.site.register(RawTable,RawtableAdmin)


class RawtableAuthoringAdmin(admin.ModelAdmin):
    list_display = ['sub_project','work_packet','sub_packet','employee_id','per_day','norm','date','project','center','sheet_name']
    list_filter = ('project','center')
    list_display_links = ('work_packet',)
admin.site.register(RawtableAuthoring,RawtableAuthoringAdmin)


class InternalerrorsAdmin(admin.ModelAdmin):
    list_display = ['work_packet','sub_project','sub_packet','audited_errors','total_errors','date','employee_id']
    list_filter = ('sub_project','work_packet','sub_packet','project','center')
    list_display_links = ('work_packet',)
admin.site.register(Internalerrors,InternalerrorsAdmin)

class InternalerrorsAuthoringAdmin(admin.ModelAdmin):
    list_display = ['sub_project','work_packet','sub_packet','employee_id','audited_errors','total_errors','date','project','center','sheet_name']
    list_filter = ('project',)
    list_display_links = ('work_packet',)
admin.site.register(InternalerrorsAuthoring,InternalerrorsAuthoringAdmin)


class ExternalerrorsAdmin(admin.ModelAdmin):
    list_display = ['sub_project','work_packet','sub_packet','audited_errors','total_errors','date','employee_id']
    list_filter = ('sub_project','work_packet','sub_packet','project','center')
admin.site.register(Externalerrors,ExternalerrorsAdmin)

class ExternalerrorsAuthoringAdmin(admin.ModelAdmin):
    #list_display = ['work_packet', 'sub_project', 'sub_packet', 'audited_errors', 'total_errors', 'date', 'employee_id','project', 'center', 'sheet_name']
    list_display = ['sub_project','work_packet','sub_packet','employee_id','audited_errors','total_errors','date','project','center','sheet_name']
    list_filter = ('project',)
    list_display_links = ('work_packet',)
admin.site.register(ExternalerrorsAuthoring,ExternalerrorsAuthoringAdmin)


class AuthoringtableAdmin(admin.ModelAdmin):
    list_display = ['sheet_name','table_schema','sheet_field','project','center','table_type']
    list_filter = ['sheet_name','project','center']
admin.site.register(Authoringtable,AuthoringtableAdmin)

class TargetsAdmin(admin.ModelAdmin):
    list_display = ['work_packet','sub_packet','from_date','to_date','target']
admin.site.register(Targets,TargetsAdmin)


class TargetsAuthoringAdmin(admin.ModelAdmin):
    list_display = ['work_packet','sub_project','sub_packet']
admin.site.register(TargetsAuthoring,TargetsAuthoringAdmin)

class WorktrackAdmin(admin.ModelAdmin):
    list_display = ['work_packet', 'opening', 'received', 'completed']
    list_filter = ['project']
admin.site.register(Worktrack,WorktrackAdmin)

class WorktrackAuthoringAdmin(admin.ModelAdmin):
    list_display = ['work_packet','sub_project','sub_packet']
    list_filter = ['project']
admin.site.register(WorktrackAuthoring,WorktrackAuthoringAdmin)


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

class UserCreationFormExtended(UserCreationForm): 
    def __init__(self, *args, **kwargs): 
        super(UserCreationFormExtended, self).__init__(*args, **kwargs) 
        self.fields['first_name'] = forms.CharField(label=_("First Name"), max_length=30)
        self.fields['last_name'] = forms.CharField(label=_("Last Name"), max_length=30)
        self.fields['email'] = forms.EmailField(label=_("E-mail"), max_length=75)

UserAdmin.add_form = UserCreationFormExtended
UserAdmin.add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
    }),
)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
