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
    list_display = ['name']
admin.site.register(TeamLead,TeamleadAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Customer,CustomerAdmin)

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

class InternalerrorsAdmin(admin.ModelAdmin):
    list_display = ['sub_project','work_packet','sub_packet','audited_errors','total_errors','date','employee_id']
    list_filter = ('sub_project','work_packet','sub_packet','project','center')
admin.site.register(Internalerrors,InternalerrorsAdmin)

class ExternalerrorsAdmin(admin.ModelAdmin):
    list_display = ['sub_project','work_packet','sub_packet','audited_errors','total_errors','date','employee_id']
    list_filter = ('sub_project','work_packet','sub_packet','project','center')
admin.site.register(Externalerrors,ExternalerrorsAdmin)

class AuthoringtableAdmin(admin.ModelAdmin):
    list_display = ['sheet_name','table_schema','sheet_field','project','center']
    list_filter = ['sheet_name','project','center']
admin.site.register(Authoringtable,AuthoringtableAdmin)

class TargetsAdmin(admin.ModelAdmin):
    list_display = ['work_packet','from_date','to_date','target']
admin.site.register(Targets,TargetsAdmin)

class WorktrackAdmin(admin.ModelAdmin):
    list_display = ['work_packet', 'opening', 'received', 'completed']
admin.site.register(Worktrack,WorktrackAdmin)

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
