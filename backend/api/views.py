import datetime
import traceback
from django.shortcuts import render
from common.utils import getHttpResponse as HttpResponse
from models import *
from django.views.decorators.csrf import csrf_exempt
from auth.decorators import loginRequired
from xlrd import open_workbook
import xlrd
from xlrd import open_workbook
from xlwt import Workbook, easyxf, XFStyle
import xlsxwriter
from src import *
from forms import *
from django.db.models import Sum
import redis
from datetime import timedelta
from datetime import date
import re
import json

def error_insert(request):
    pass
def get_order_of_headers(open_sheet, Default_Headers, mandatory_fileds=[]):
    indexes, sheet_indexes = {}, {}
    sheet_headers = open_sheet.row_values(0)
    lower_sheet_headers = [i.lower() for i in sheet_headers]
    if not mandatory_fileds:
        mandatory_fileds = Default_Headers

    max_index = len(sheet_headers)
    is_mandatory_available = set([i.lower() for i in mandatory_fileds]) - set([j.lower() for j in sheet_headers])
    for ind, val in enumerate(Default_Headers):
        val = val.lower()
        if val in lower_sheet_headers:
            ind_sheet = lower_sheet_headers.index(val)
            sheet_indexes.update({val: ind_sheet})
        else:
            ind_sheet = max_index
            max_index += 1
        #comparing with lower case for case insensitive
        #Change the code as declare *_XL_HEADEERS and *_XL_MAN_HEADERS
        indexes.update({val: ind_sheet})
    return is_mandatory_available, sheet_indexes, indexes

def validate_sheet(open_sheet, request, SOH_XL_HEADERS, SOH_XL_MAN_HEADERS):
    sheet_headers = []
    if open_sheet.nrows > 0:
        is_mandatory_available, sheet_headers, all_headers = get_order_of_headers(open_sheet, SOH_XL_HEADERS, SOH_XL_MAN_HEADERS)
        sheet_headers = sorted(sheet_headers.items(), key=lambda x: x[1])
        all_headers = sorted(all_headers.items(), key=lambda x: x[1])
        if is_mandatory_available:
            status = ["Fields are not available: %s" % (", ".join(list(is_mandatory_available)))]
            #index_status.update({1: status})
            return "Failed", status
    else:
        status = "Number of Rows: %s" % (str(open_sheet.nrows))
        index_status.update({1: status})
    return sheet_headers

def get_cell_data(open_sheet, row_idx, col_idx):
    try:
        cell_data = open_sheet.cell(row_idx, col_idx).value
        cell_data = str(cell_data)
        if isinstance(cell_data, str):
            cell_data = cell_data.strip()
    except IndexError:
        cell_data = ''
    return cell_data

#@loginRequired
def project(request):
    user_group = request.user.groups.values_list('name', flat=True)[0]
    dict = {}
    if 'team_lead' in user_group:
        prj_id = TeamLead.objects.filter(name_id=request.user.id).values_list('project')[0][0]
        project = str(Project.objects.filter(id=prj_id)[0])
        return HttpResponse(project)
    if 'center_manager' in user_group:
        center = Centermanager.objects.filter(name_id=request.user.id).values_list('center', flat=True)[0]
        center_name = Center.objects.filter(id=center).values_list('name', flat=True)[0]
        project_names = Project.objects.filter(center_id=center).values_list('name', flat=True)
        var = [x.encode('UTF8') for x in project_names]
        dict['center'] = center_name
        dict['project'] = var
        dict['role'] = user_group
        return HttpResponse(dict)
    if 'nextwealth_manager' in user_group:
        center_name = Center.objects.values_list('id', flat=True)
        dict['role'] = user_group
        dict['cen_pro'] = {}
        dict['centers'] = []

        for center in center_name:
            cant_name = Center.objects.filter(id=center).values_list('name', flat=True)[0]
            project_names = Project.objects.filter(center_id=center).values_list('name', flat=True)
            var = {}
            for x in project_names:
                if 'Probe' in x:
                    var[x.encode('UTF8')] = 'page1'
                if 'Realshopee' in x:
                    var[x.encode('UTF8')] = 'page2'
                if 'Dell' in x:
                    var[x.encode('UTF8')] = 'page3'
            #var = [x.encode('UTF8') for x in project_names]
            dict['centers'].append(cant_name)
            dict['cen_pro'][cant_name] = var
        return HttpResponse(dict)
    if 'customer' in user_group:
        details = {}
        select_list = []
        layout_list = []
        center_list = Customer.objects.filter(name_id=request.user.id).values_list('center')
        project_list = Customer.objects.filter(name_id=request.user.id).values_list('project')
        if (len(center_list) & len(project_list)) == 1:
            select_list.append('none')
        if len(center_list) < 2:
            center_name = str(Center.objects.filter(id=center_list[0][0])[0])
            for project in project_list:
                project_name = str(Project.objects.filter(id=project[0])[0])
                lay_list = json.loads(str(Project.objects.filter(id=project[0]).values_list('layout')[0][0]))
                vari = center_name + ' - ' + project_name
                layout_list.append({vari:lay_list})
                select_list.append(vari)
        elif len(center_list) >= 2:
            for center in center_list:
                center_name = str(Center.objects.filter(id=center[0])[0])
                for project in project_list:
                    project_name = str(Project.objects.filter(id=project[0])[0])
                    select_list.append(center_name + ' - ' + project_name)
        details['list'] = select_list
        details['role'] = 'customer'
        details['lay'] = layout_list
        return HttpResponse(details)

def redis_insert(prj_obj,center_obj,dates_list,key_type):
    prj_name = prj_obj.name
    center_name = center_obj.name
    data_dict = {}
    #dates_list = RawTable.objects.filter(project=prj_obj,center=center_obj).values_list('date').distinct()
    all_dates = []
    for date in dates_list:
        #part_date = str(date[0].date())
        part_date = str(date)
        all_dates.append(part_date)
        #volumes_list = RawTable.objects.filter(date=date[0],project=prj_obj,center=center_obj ).values_list('volume_type').distinct()

        if key_type == 'Production':
            volumes_list = RawTable.objects.filter(project=prj_obj,center=center_obj,date=date ).values('sub_project','work_packet','sub_packet','date')
        if key_type == 'Internal':
            volumes_list = Internalerrors.objects.filter(project=prj_obj,center=center_obj, date=date).values('sub_project','work_packet','sub_packet', 'date')
        if key_type == 'External':
            volumes_list = Externalerrors.objects.filter(project=prj_obj, center=center_obj, date=date).values('sub_project', 'work_packet', 'sub_packet', 'date')
        for row_record_dict in volumes_list:
            single_row_dict={}
            for vol_key,vol_value in row_record_dict.iteritems():
                if vol_value=='':
                    single_row_dict[vol_key]='NA'
                else:
                    single_row_dict[vol_key] =vol_value
            value_dict = {}
            if key_type=='Production':
                redis_key = '{0}_{1}_{2}_{3}_{4}_{5}'.format(prj_name,center_name,single_row_dict['sub_project'],single_row_dict['work_packet'],single_row_dict['sub_packet'],str(single_row_dict['date']))
                total = RawTable.objects.filter(sub_project=row_record_dict['sub_project'],work_packet=row_record_dict['work_packet'],
                                                sub_packet=row_record_dict['sub_packet'],date=date).values_list('per_day').aggregate(Sum('per_day'))
                value_dict[str(single_row_dict['sub_project']+'_'+single_row_dict['work_packet']+'_'+single_row_dict['sub_packet'])] = str(total['per_day__sum'])
                data_dict[redis_key] = value_dict
            if key_type == 'Internal':
                redis_key = '{0}_{1}_{2}_{3}_{4}_{5}_error'.format(prj_name, center_name, single_row_dict['sub_project'],single_row_dict['work_packet'],single_row_dict['sub_packet'], str(single_row_dict['date']))
                total_audit = Internalerrors.objects.filter(sub_project=row_record_dict['sub_project'],
                                                work_packet=row_record_dict['work_packet'],
                                                sub_packet=row_record_dict['sub_packet'], date=date).values_list('audited_errors').aggregate(Sum('audited_errors'))
                total_errors = Internalerrors.objects.filter(sub_project=row_record_dict['sub_project'],
                                                             work_packet=row_record_dict['work_packet'],
                                                             sub_packet=row_record_dict['sub_packet'],
                                                             date=date).values_list('total_errors').aggregate(Sum('total_errors'))
                value_dict['total_audit'] = str(total_audit['audited_errors__sum'])
                value_dict['total_errors'] = str(total_errors['total_errors__sum'])
                data_dict[redis_key] = value_dict
            if key_type == 'External':
                redis_key = '{0}_{1}_{2}_{3}_{4}_{5}_externalerror'.format(prj_name, center_name,single_row_dict['sub_project'],single_row_dict['work_packet'],single_row_dict['sub_packet'], str(single_row_dict['date']))
                total_audit = Externalerrors.objects.filter(sub_project=row_record_dict['sub_project'],
                                                            work_packet=row_record_dict['work_packet'],
                                                            sub_packet=row_record_dict['sub_packet'],
                                                            date=date).values_list('audited_errors').aggregate(Sum('audited_errors'))
                total_errors = Externalerrors.objects.filter(sub_project=row_record_dict['sub_project'],
                                                             work_packet=row_record_dict['work_packet'],
                                                             sub_packet=row_record_dict['sub_packet'],
                                                             date=date).values_list('total_errors').aggregate(Sum('total_errors'))
                value_dict['total_audit'] = str(total_audit['audited_errors__sum'])
                value_dict['total_errors'] = str(total_errors['total_errors__sum'])
                data_dict[redis_key] = value_dict

    print data_dict,all_dates
    conn = redis.Redis(host="localhost", port=6379, db=0)
    current_keys = []
    for key,value in data_dict.iteritems():
        current_keys.append(key)
        conn.hmset(key,value)
    return "hai"
def redis_insert_two(prj_obj,center_obj,key_type):
    prj_name = prj_obj.name
    center_name = center_obj.name
    data_dict = {}
    #volumes_list = Error.objects.values_list('volume_type',flat=True).distinct()
    if (prj_name in ['Dell','Dellcoding','DellBilling'] and key_type=='Internal') or (prj_name in ['Probe'] and key_type=='Internal'):
        volumes_list = Error.objects.filter(project=prj_obj,center=center_obj).values_list('volume_type',flat=True).distinct()
        error_type = 'error'
    if (prj_name in ['Dell','Dellcoding'] and key_type=='External'):
        volumes_list = Externalerrors.objects.filter(project=prj_obj, center=center_obj).values_list('volume_type',flat=True).distinct()
        error_type = 'externalerror'
    audited_values,total_errors = [],[]
    for volume in volumes_list:
        value_dict = {}
        dates_values = Error.objects.filter(volume_type=volume,project=prj_obj,center=center_obj).values_list('date',flat=True)
        for date in dates_values:
            error_data = {}
            redis_key = '{0}_{1}_{2}_{3}_{4}'.format(prj_name,center_name, volume, date,error_type)
            if key_type=='Internal':
                audited_values = Error.objects.filter(date=date,volume_type=volume,project=prj_obj,center=center_obj).values_list('audited_errors',flat=True)
                total_errors = Error.objects.filter(date=date,volume_type=volume,project=prj_obj,center=center_obj).values_list('error_value',flat=True)
            if key_type=='External':
                audited_values = Externalerrors.objects.filter(date=date,volume_type=volume,project=prj_obj,center=center_obj).values_list('audited_errors',flat=True)
                total_errors = Externalerrors.objects.filter(date=date,volume_type=volume,project=prj_obj,center=center_obj).values_list('error_value',flat=True)
            error_data['audited_values'] = int(sum(audited_values))
            error_data['total_errors'] = int(sum(total_errors))
            print error_data
            data_dict[redis_key]=error_data

    print data_dict


    conn = redis.Redis(host="localhost", port=6379, db=0)
    current_keys = []
    for key, value in data_dict.iteritems():
        current_keys.append(key)
        conn.hmset(key, value)
    return data_dict
def redis_insert_three(prj_obj,center_obj):
    prj_name = prj_obj.name
    center_name = center_obj.name
    data_dict = {}
    volumes_list = Externalerrors.objects.filter(project=prj_obj,center=center_obj).values_list('volume_type',flat=True).distinct()
    for volume in volumes_list:
        value_dict = {}
        dates_values = Externalerrors.objects.filter(volume_type=volume,project=prj_obj,center=center_obj).values_list('date',flat=True).distinct()
        for date in dates_values:
            extr_error_data = {}
            redis_key = '{0}_{1}_{2}_{3}_externalerror'.format(prj_name,center_name, volume, date)
            avoidable_count = 0
            concept_count = 0
            total_error_count = 0
            extranal_data = Externalerrors.objects.filter(date=date,volume_type=volume,project=prj_obj,center=center_obj).values('error_type','error_value','agent_reply')
            for ex_data in extranal_data:
                #import pdb;pdb.set_trace()
                if ex_data['agent_reply'] in ['Reverted']:
                    if ex_data['error_type']== 'avoidable':
                        avoidable_count = avoidable_count+int(ex_data['error_value'])
                        total_error_count = int(ex_data['error_value']) + total_error_count
                    if ex_data['error_type']== 'concept':
                        concept_count = concept_count+ int(ex_data['error_value'])
                else :
                    if ex_data['error_type']== 'avoidable':
                        avoidable_count = avoidable_count+int(ex_data['error_value'])
                        #total_error_count = int(ex_data['error_value']) + total_error_count
                    if ex_data['error_type']== 'concept':
                        concept_count = concept_count+ int(ex_data['error_value'])
                    total_error_count = int(ex_data['error_value']) + total_error_count
            extr_error_data['avoidable'] = avoidable_count
            extr_error_data['concept'] = concept_count
            extr_error_data['total_errors'] = total_error_count
            print extr_error_data
            data_dict[redis_key]= extr_error_data

    print data_dict

    conn = redis.Redis(host="localhost", port=6379, db=0)
    current_keys = []
    for key, value in data_dict.iteritems():
        current_keys.append(key)
        conn.hmset(key, value)
    return "hai"
def upload(request):
    """if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES['myfile'])
        if form.is_valid:
            newdoc = Document(document=request.FILES['myfile'])
            var = "general"
            newdoc.save()"""
    teamleader_obj_name = TeamLead.objects.filter(name_id=request.user.id)[0]
    teamleader_obj = TeamLead.objects.filter(name_id=request.user.id).values_list('project_id','center_id')[0]
    prj_obj = Project.objects.filter(id=teamleader_obj[0])[0]
    prj_name= prj_obj.name
    center_obj = Center.objects.filter(id=teamleader_obj[1])[0]
    fname = request.FILES['myfile']
    var = fname.name.split('.')[-1].lower()
    if var not in ['xls', 'xlsx', 'xlsb']:
        return HttpResponse("Invalid File")
    else:
        try:
            open_book = open_workbook(filename=None, file_contents=fname.read())
            #open_sheet = open_book.sheet_by_index(0)
        except:
            return HttpResponse("Invalid File")
        excel_sheet_names = open_book.sheet_names()
        file_sheet_names = Authoringtable.objects.filter(project=prj_obj,center=center_obj).values_list('sheet_name',flat=True).distinct()
        #file_sheet_names = [x.encode('UTF8') for x in file_sheet_name]
        sheet_index_dict = {}
        for sh_name in file_sheet_names:
            if sh_name in excel_sheet_names:
                sheet_index_dict[sh_name] = open_book.sheet_names().index(sh_name)
        for key,value in sheet_index_dict.iteritems():
            one_sheet_data = {}
            prod_date_list,internal_date_list,external_date_list=[],[],[]
            open_sheet = open_book.sheet_by_index(value)
            SOH_XL_HEADERS = open_sheet.row_values(0)
            main_headers = Authoringtable.objects.filter(sheet_name=key,project=prj_obj,center=center_obj).values_list('sheet_field',flat=True)
            #sheet_main_headers = [x.encode('UTF8') for x in main_headers]
            sheet_main_headers = main_headers
            table_schema = Authoringtable.objects.filter(sheet_name=key,project=prj_obj,center=center_obj).values_list('table_schema',flat=True)
            #table_schema = [x.encode('UTF8') for x in table_schema]
            mapping_table = {}
            for sh_filed,t_field in zip(sheet_main_headers,table_schema):
                mapping_table[sh_filed] = t_field
            SOH_XL_MAN_HEADERS = [x.title() for x in main_headers]
            sheet_headers = validate_sheet(open_sheet,request,SOH_XL_HEADERS,SOH_XL_MAN_HEADERS)
            #import pdb;pdb.set_trace()
            for row_idx in range(1, open_sheet.nrows):
                error_type = {}
                raw_sheet_data = {}
                customer_data = {}
                for column, col_idx in sheet_headers:
                    #import pdb;pdb.set_trace()
                    cell_data = get_cell_data(open_sheet, row_idx, col_idx)
                    column_name = mapping_table.get(column, '')
                    if column in ["date", "from date","to date"]:
                        cell_data = xlrd.xldate_as_tuple(int(cell_data.split('.')[0]), 0)
                        cell_data = '%s-%s-%s' % (cell_data[0], cell_data[1], cell_data[2])
                        customer_data[column_name] = ''.join(cell_data)
                        raw_sheet_data[column_name] = ''.join(cell_data)
                    elif column !="date," and column in mapping_table.keys():
                        customer_data[column_name] = ''.join(cell_data)
                        raw_sheet_data[column_name] = ''.join(cell_data)


                """if prj_name in ['Probe','Dell']:
                volume_dict = {'DataDownload':'DD', 'CompanyCoordinates':'CC' , 'DetailFinancial':'DF','GroupCompanies':'GC','FES':'FES' ,
                               'Legal & CDR':'Legal' ,'DetailFinancial with FES':'DFES','Charges':'Charges',
                               'Compliance':'Compliance' ,'LLP':'LLP','Manual Download' : 'MD'}
                if customer_data.get('volume_type','') in volume_dict.keys():
                    customer_data['volume_type'] = volume_dict[customer_data['volume_type']]"""

                #import pdb;pdb.set_trace()
                new_can = 0
                if key in ['Production']:
                    rec_status = 0
                    if customer_data.has_key('target')==False:
                        customer_data['target'] = 0
                    per_day_value = int(float(customer_data['work_done']))
                    prod_date_list.append(customer_data['date'])
                    new_can = RawTable(project=prj_obj, sub_project=customer_data.get('sub_project',''),work_packet=customer_data['work_packet'],
                                       sub_packet=customer_data.get('sub_packet', ''),employee_id=customer_data.get('emp_id',''),per_hour=0,
                                       per_day=per_day_value,date=customer_data['date'], norm=int(float(customer_data['target'])),
                                       team_lead=teamleader_obj_name,center = center_obj)
                if key in ['Internal']:
                    if customer_data.has_key('audited_count')==False:
                        customer_data['audited_count'] = 0
                    internal_date_list.append(customer_data['date'])
                    new_can = Internalerrors(employee_id=customer_data.get('emp_id',''),
                                             sub_project=customer_data.get('sub_project', ''),
                                             work_packet=customer_data['work_packet'],
                                             sub_packet=customer_data.get('sub_packet', ''),date=customer_data['date'],
                                             audited_errors=int(float(customer_data.get('audited_count',''))),
                                             total_errors=int(float(customer_data['total_errors'])),
                                             project=prj_obj,center=center_obj,error_name=customer_data.get('error_name',''))

                if key in ['External'] :
                    if customer_data.has_key('audited_count')==False:
                        customer_data['audited_count'] = 0
                    external_date_list.append(customer_data['date'])
                    new_can = Externalerrors(employee_id=customer_data.get('emp_id',''),
                                             sub_project=customer_data.get('sub_project', ''),
                                             work_packet=customer_data['work_packet'],
                                             sub_packet=customer_data.get('sub_packet', ''),date=customer_data['date'],
                                             audited_errors=int(float(customer_data.get('audited_count',''))),
                                             total_errors=int(float(customer_data['total_errors'])),
                                             project=prj_obj,center=center_obj,error_name=customer_data.get('error_name',''))
                if key in ['Targets'] :
                    #import pdb;pdb.set_trace()
                    new_can = Targets(sub_project=customer_data.get('sub_project', ''),
                                             work_packet=customer_data['work_packet'],
                                             sub_packet=customer_data.get('sub_packet', ''),
                                             from_date=customer_data['from_date'],
                                             to_date = customer_data['to_date'],
                                             target = int(float(customer_data['target'])),project=prj_obj,center=center_obj)
                if key in ['Work Track']:
                    new_can = Worktrack(
                        sub_project=customer_data.get('sub_project', ''),
                        work_packet=customer_data['work_packet'],
                        sub_packet=customer_data.get('sub_packet', ''),
                        date=customer_data['date'],
                        opening=int(float(customer_data['opening'])), received=int(float(customer_data['received'])),
                        non_workable_count=int(float(customer_data['non_workable_count'])),
                        completed=int(float(customer_data['completed'])), closing_balance=int(float(customer_data['closing_balance'])),
                        project=prj_obj, center=center_obj)


                if new_can:
                    try:
                        print customer_data
                        new_can.save()
                    except:
                        pass
                        #var = 'Duplicate Sheet'
                        #return HttpResponse(var)
            if key in ['Production','Rawdata']:
                insert = redis_insert(prj_obj,center_obj,prod_date_list,key_type='Production')
            if key == 'Internal':
                #insert = redis_insert_two(prj_obj,center_obj,key_type='Internal')
                insert = redis_insert(prj_obj, center_obj, internal_date_list,key_type='Internal')
            if key == 'External':
                insert = redis_insert(prj_obj, center_obj,external_date_list, key_type='External',)
            if key in ['Error','Rawdata'] and prj_name in ['Dell','Dellcoding']:
                pass
                #insert = redis_insert_two(prj_obj, center_obj,key_type='External')
                #insert = redis_insert_two(prj_obj, center_obj, key_type='Internal')
            elif key == 'Error' and prj_name in ['Probe']:
                pass
                #insert = redis_insert_three(prj_obj,center_obj)
        return HttpResponse(var)




def sheet_upload_one(prj_obj,center_obj,teamleader_obj,key,one_sheet_data):
    customer_data={}
    work_packets = ['CAMC - XRAYS','CAMC']
    new_can = 0
    print one_sheet_data
    for data_key,data_value in one_sheet_data.iteritems():
        internal_errors = {}
        external_errors = {}
        #print data_value
        for data_dict in data_value:
            print data_dict
            if data_dict['work_packet'] in work_packets :
                volume_type = '{0}_{1}'.format(data_dict['project'], data_dict['work_packet']).replace(' ','')
                try:
                    per_day_value = int(float(data_dict['count']))
                except:
                    per_day_value = 0
                norm = 833
                new_can = RawTable(project=prj_obj, employee=data_dict.get('emp_id', ''),
                                   volume_type=volume_type, per_hour=0, per_day=per_day_value,
                                   date=data_dict['date'], norm=norm,
                                   team_lead=teamleader_obj, center=center_obj)
                new_can.save()
            if ('Internal' in data_dict['work_packet']):
                internal_errors[data_dict['work_packet']] = data_dict['count']
                internal_errors['volume_type'] = data_dict['project']
            if 'External' in data_dict['work_packet'] :
                external_errors[data_dict['work_packet']] = data_dict['count']
                external_errors['volume_type'] = data_dict['project']
        if internal_errors:
            new_can = Error(employee_id=internal_errors.get('emp_id', ''),
                            volume_type=internal_errors['volume_type'].replace(' ',''),
                            date=data_key, audited_errors=int(float(internal_errors['Internal Audited'])),
                            error_value=int(float(internal_errors['Internal Error'])), project=prj_obj,
                            center=center_obj, error_type=internal_errors.get('error_name',''))
            new_can.save()
        if external_errors :
            new_can = Externalerrors(employee_id=external_errors.get('emp_id', ''),
                                     volume_type=external_errors['volume_type'].replace(' ',''),
                                     date=data_key, audited_errors=int(float(external_errors['External Audited'])),
                                     error_value=int(float(external_errors['External Error'])), project=prj_obj,
                                     center=center_obj, error_type=external_errors.get('error_name',''))
            new_can.save()


def user_data(request):
    user_group = request.user.groups.values_list('name',flat=True)[0]
    manager_dict = {}
    if 'Center_Manager' in user_group:
        center_id = Centermanager.objects.filter(name_id=request.user.id).values_list('center_name', flat=True)
        center_name = Center.objects.filter(id = center_id).values_list('name',flat=True)[0]
        project = Center.objects.filter(name = str(center_name)).values_list('project_name_id',flat=True)
        project_names = Project.objects.filter(id__in = project).values_list('name',flat=True)
        manager_dict[center_name]= str(project_names)
    if 'Nextwealth_Manager' in user_group:
        center_id = Nextwealthmanager.objects.filter(id=request.user.id).values_list('center_name')
        print center_id
    return HttpResponse(manager_dict)


def graph_data_alignment(volumes_data,name_key):
    productivity_series_list = []
    for vol_name, vol_values in volumes_data.iteritems():
        if isinstance(vol_values, float):
            vol_values = float('%.2f' % round(vol_values, 2))
        prod_dict = {}
        prod_dict['name'] = vol_name.replace('NA_','').replace('_NA','')
        if name_key == 'y':
            prod_dict[name_key] = vol_values
        if name_key == 'data':
            if isinstance(vol_values, list):
                prod_dict[name_key] = vol_values
            else:
                prod_dict[name_key] = [vol_values]
        productivity_series_list.append(prod_dict)

    return productivity_series_list


def graph_data_alignment_other(volumes_data, work_packets, name_key):
    productivity_series_list = {}
    for vol_name, vol_values in volumes_data.iteritems():
        prod_main_dict={}
        prod_main_dict['x_axis']=[vol_name]
        prod_inner_dict = {}
        prod_inner_dict['name'] = vol_name
        prod_inner_dict[name_key] =vol_values
        prod_main_dict['y_axis'] = prod_inner_dict
        # productivity_series_list.append(prod_dict)
        productivity_series_list[vol_name] = prod_main_dict
    if len(work_packets)<=1:
        return productivity_series_list
    if len((work_packets))>=2:
        if work_packets[0] in productivity_series_list.keys() and work_packets[1] in productivity_series_list.keys():
            prod_main_dict = {}
            prod_main_dict['x_axis'] = [work_packets[0],work_packets[1]]
            prod_inner_dict = {}
            prod_inner_dict[work_packets[0]] = productivity_series_list[work_packets[0]]['y_axis']
            prod_inner_dict[work_packets[1]] = productivity_series_list[work_packets[1]]['y_axis']
            prod_main_dict['y_axis'] = prod_inner_dict
            productivity_series_list[work_packets[0]] = prod_main_dict
        return productivity_series_list


def product_total_graph(date_list,prj_id,center_obj,work_packets):
    work = work_packets
    conn = redis.Redis(host="localhost", port=6379, db=0)
    result = {}
    volumes_dict = {}
    date_values = {}
    #volume_list = RawTable.objects.filter(project=prj_id,center=center_obj).values_list('volume_type', flat=True).distinct()
    prj_name = Project.objects.filter(id=prj_id).values_list('name',flat=True)
    center_name = Center.objects.filter(id=center_obj).values_list('name', flat=True)
    for date_va in date_list:
        #below code for product,wpf graphs
        volume_list = RawTable.objects.filter(project=prj_id, center=center_obj).values('sub_project','work_packet','sub_packet').distinct()
        for vol_type in volume_list:
            for vol_keys, vol_values in vol_type.iteritems():
                if vol_values == '':
                    vol_type[vol_keys] = 'NA'
            work_packets = vol_type['sub_project'] +'_' +vol_type['work_packet']+'_'+ vol_type['sub_packet']
            date_pattern = '{0}_{1}_{2}_{3}'.format(prj_name[0], str(center_name[0]), str(work_packets), date_va)
            key_list = conn.keys(pattern=date_pattern)
            if not key_list:
                if date_values.has_key(work_packets):
                    date_values[work_packets].append(0)
                else:
                    date_values[work_packets] = [0]
            for cur_key in key_list:
                var = conn.hgetall(cur_key)
                for key,value in var.iteritems():
                    if date_values.has_key(key):
                        date_values[key].append(int(value))
                    else:
                        date_values[key]=[int(value)]
                volumes_dict['data'] = date_values
                volumes_dict['date'] = date_list
                result['data'] = volumes_dict

    print volumes_dict
    #below code is to generate productivity chcart format
    volumes_data = result['data']['data']
    #productivity_series_list = graph_data_alignment_other(volumes_data,work,name_key='data')
    #productivity_series_list = graph_data_alignment(volumes_data,name_key='data')
    result['prod_days_data'] = volumes_data
    volume_bar_data = {}
    volume_bar_data['volume_type']= volumes_data.keys()
    volume_keys_data ={}
    for key,value in volumes_data.iteritems():
        volume_keys_data[key]= sum(value)
    volume_list_data=[]
    volume_dict = {}

    for key,value in volume_keys_data.iteritems() :
        new_list=[]
        if 'DetailFinancial' not in key:
            if volume_dict.has_key(key):
                new_list.append(volume_dict[key])
            else:
                new_list.append(key)
            new_list.append(value)
            volume_list_data.append(new_list)
    volume_bar_data['volume_new_data']=volume_list_data
    volume_bar_data['volume_values'] = volume_keys_data
    result['volumes_data'] = volume_bar_data
    print result
    return result



def internal_extrnal_graphs_same_formula(request,date_list,prj_id,center_obj,err_type):
    prj_name = Project.objects.filter(id=prj_id).values_list('name', flat=True)
    center_name = Center.objects.filter(id=center_obj).values_list('name', flat=True)
    if err_type =='Internal' :
        extr_volumes_list = Internalerrors.objects.filter(project=prj_id, center=center_obj).values('sub_project','work_packet','sub_packet').distinct()
        err_key_type = 'error'
    if err_type == 'External':
        extr_volumes_list = Externalerrors.objects.filter(project=prj_id, center=center_obj).values('sub_project','work_packet','sub_packet').distinct()
        err_key_type = 'externalerror'
    conn = redis.Redis(host="localhost", port=6379, db=0)
    # below variable for error graphs.
    result = {}
    vol_error_values = {}
    vol_audit_data = {}
    # below variable for external errors
    extrnl_error_values = {}
    extrnl_err_type = {}
    extr_volumes_list_new=[]
    for date_va in date_list:
        for vol_type in extr_volumes_list:
            for vol_keys, vol_values in vol_type.iteritems():
                if vol_values == '':
                    vol_type[vol_keys] = 'NA'
            work_packets = vol_type['sub_project'] + '_' + vol_type['work_packet'] + '_' + vol_type['sub_packet']
            extr_volumes_list_new.append(work_packets)
            key_pattern = '{0}_{1}_{2}_{3}_{4}'.format(prj_name[0], str(center_name[0]), work_packets, date_va,err_key_type)
            audit_key_list = conn.keys(pattern=key_pattern)
            for cur_key in audit_key_list:
                var = conn.hgetall(cur_key)
                for key, value in var.iteritems():
                    error_vol_type = work_packets
                    if key == 'total_errors':
                        if vol_error_values.has_key(error_vol_type):
                            vol_error_values[error_vol_type].append(int(value))
                        else:
                            vol_error_values[error_vol_type] = [int(value)]
                    else:
                        if vol_audit_data.has_key(error_vol_type):
                            vol_audit_data[error_vol_type].append(int(value))
                        else:
                            vol_audit_data[error_vol_type] = [int(value)]
    volume_dict = {}
    # error_dist_vol = Error.objects.values_list('volume_type', flat=True).distinct()
    #error_dist_vol = Externalerrors.objects.filter(project=prj_id, center=center_obj).values_list('volume_type',flat=True).distinct()
    error_volume_data = {}
    error_graph_data = []
    for key, value in vol_error_values.iteritems():
        error_graph = []
        error_volume_data[key] = sum(value)
        error_graph.append(key)
        error_graph.append(sum(value))
        error_graph_data.append(error_graph)
    error_audit_data = {}
    for key, value in vol_audit_data.iteritems():
        error_audit_data[key] = sum(value)
    error_accuracy = {}
    for volume in extr_volumes_list_new:
        if (volume in error_volume_data.keys()) and (volume in error_audit_data.keys()) and (error_audit_data[volume] > 0):
            percentage = (float(error_volume_data[volume]) / error_audit_data[volume]) * 100
            #percentage = 100 - float('%.2f' % round(percentage, 2))
            percentage = 100 - float('%.2f' % round(percentage, 2))
            error_accuracy[volume] = percentage
    total_graph_data = {}
    if err_type == 'Internal':
        #result['internal_error_count'] = graph_data_alignment(error_volume_data, name_key='y')
        #result['internal_accuracy_graph'] = graph_data_alignment(error_accuracy, name_key='data')
        result['internal_error_count'] = error_volume_data
        result['internal_accuracy_graph'] = error_accuracy

    if err_type == 'External':
        #result['external_error_count'] = graph_data_alignment(error_volume_data, name_key='y')
        #result['external_accuracy_graph'] = graph_data_alignment(error_accuracy, name_key='data')
        result['external_error_count'] = error_volume_data
        result['external_accuracy_graph'] = error_accuracy

    return result

    # below code for external graphs


def externalerror_graph(request,date_list,prj_id,center_obj,packet_sum_data):
    prj_name = Project.objects.filter(id=prj_id).values_list('name', flat=True)
    center_name = Center.objects.filter(id=center_obj).values_list('name', flat=True)
    extr_volumes_list = Externalerrors.objects.filter(project=prj_id, center=center_obj).values('sub_project','work_packet','sub_packet').distinct()
    extr_volumes_list_new = []
    conn = redis.Redis(host="localhost", port=6379, db=0)
    # below variable for error graphs.
    result = {}
    vol_error_values = {}
    vol_audit_data = {}
    # below variable for external errors
    extrnl_error_values = {}
    extrnl_err_type = {}
    for date_va in date_list:
        # below code for internal error
        for vol_type in extr_volumes_list:
            for vol_keys, vol_values in vol_type.iteritems():
                if vol_values == '':
                    vol_type[vol_keys] = 'NA'
            work_packets = vol_type['sub_project'] + '_' + vol_type['work_packet'] + '_' + vol_type['sub_packet']
            extr_volumes_list_new.append(work_packets)
            #extr_key_pattern = '*{0}*_externalerror'.format(date_va)
            extr_key_pattern =  '{0}_{1}_{2}_{3}_externalerror'.format(prj_name[0], str(center_name[0]), work_packets, date_va)
            extr_key_list = conn.keys(pattern=extr_key_pattern)

            for cur_key in extr_key_list:
                var = conn.hgetall(cur_key)
                for key, value in var.iteritems():
                    #import pdb;pdb.set_trace()
                    error_vol_type = work_packets
                    if key == 'total_errors':
                        if extrnl_error_values.has_key(error_vol_type):
                            extrnl_error_values[error_vol_type].append(int(value))
                        else:
                            extrnl_error_values[error_vol_type] = [int(value)]
                    else:
                        if extrnl_err_type.has_key(error_vol_type):
                            extrnl_err_type[error_vol_type].append(int(value))
                        else:
                            extrnl_err_type[error_vol_type] = [int(value)]
    volume_dict = {}
    extrnl_error_sum = {}
    for key, value in extrnl_error_values.iteritems():
        extrnl_error_sum[key] = sum(value)

    # beow code for external erro accuracy
    packet_sum_data = packet_sum_data
    extr_err_accuracy = {}
    for er_key, er_value in extrnl_error_sum.iteritems():
        if packet_sum_data.has_key(er_key):
            if packet_sum_data[er_key] != 0:
                percentage = (float(er_value) / packet_sum_data[er_key]) * 100
                percentage = 100 - float('%.2f' % round(percentage, 2))
                extr_err_accuracy[er_key] = [percentage]
            else:
                extr_err_accuracy[er_key] = [0]
    #volume_list = RawTable.objects.values_list('volume_type', flat=True).distinct()
    extr_err_acc_name = []
    extr_err_acc_perc = []
    for key, value in extr_err_accuracy.iteritems():
        extr_err_acc_name.append(key)
        extr_err_acc_perc.append(value[0])
    err_type_keys = []
    err_type_avod = []
    err_type_concept = []
    """for key, value in extrnl_err_type.iteritems():
        err_type_keys.append(key)
        for avod_key, avod_value in value.iteritems():
            extrnl_err_type[key][avod_key] = sum(avod_value)
            if avod_key == 'avoidable':
                err_type_avod.append(extrnl_err_type[key][avod_key])
            if avod_key == 'concept':
                err_type_concept.append(extrnl_err_type[key][avod_key])
    result['error_types'] = {}
    result['error_types']['err_type_keys'] = err_type_keys
    result['error_types']['err_type_avod'] = err_type_avod
    result['error_types']['err_type_concept'] = err_type_concept"""
    result['extr_err_accuracy'] = {}
    #result['extr_err_accuracy']['packets_percntage'] = graph_data_alignment(extr_err_accuracy, name_key='data')
    result['extr_err_accuracy']['packets_percntage'] = extr_err_accuracy
    result['extr_err_accuracy']['extr_err_name'] = extr_err_acc_name
    result['extr_err_accuracy']['extr_err_perc'] = extr_err_acc_perc
    if 'DFES' in extrnl_error_sum:
        del extrnl_error_sum['DFES']
    result['extrn_error_count'] = graph_data_alignment(extrnl_error_sum, name_key='y')
    # print result
    return result


def internal_extrnal_graphs(request,date_list,prj_id,center_obj,packet_sum_data):
    prj_name = Project.objects.filter(id=prj_id).values_list('name', flat=True)
    center_name = Center.objects.filter(id=center_obj).values_list('name', flat=True)
    #import pdb;pdb.set_trace()
    final_internal_data = internal_extrnal_graphs_same_formula(request, date_list, prj_id, center_obj,err_type='Internal')
    if prj_name[0] in ['Dell','DellCoding','DellBilling']:
        final_external_data = internal_extrnal_graphs_same_formula(request, date_list, prj_id, center_obj,err_type='External')
        final_internal_data.update(final_external_data)
        return final_internal_data
    if prj_name[0] in ['Probe','Ujjivan']:
        final_external_data = externalerror_graph(request, date_list, prj_id, center_obj,packet_sum_data)
        final_internal_data.update(final_external_data)
        return final_internal_data
    result={}
    #return result

def day_week_month(request,dwm_dict,prj_id,center,work_packets):
    if dwm_dict.has_key('day'):
        final_dict = {}
        result_dict = product_total_graph(dwm_dict['day'],prj_id,center,work_packets)
        if len(result_dict['prod_days_data'])>0:
            result_dict['productivity_data'] = graph_data_alignment(result_dict['prod_days_data'],name_key='data')
        packet_sum_data = result_dict['volumes_data']['volume_values']
        error_graphs_data = internal_extrnal_graphs(request, dwm_dict['day'], prj_id, center, packet_sum_data)
        all_external_error_accuracy={}
        if error_graphs_data.has_key('internal_accuracy_graph'):
            final_dict['internal_accuracy_graph'] = graph_data_alignment(error_graphs_data['internal_accuracy_graph'], name_key='y')
        if error_graphs_data.has_key('extr_err_accuracy'):
            for vol_key, vol_values in error_graphs_data['extr_err_accuracy']['packets_percntage'].iteritems():
                all_external_error_accuracy[vol_key]=vol_values[0]
            final_dict['external_accuracy_graph'] = graph_data_alignment(all_external_error_accuracy,name_key='y')
        if error_graphs_data.has_key('external_accuracy_graph'):
            final_dict['external_accuracy_graph'] = graph_data_alignment(error_graphs_data['external_accuracy_graph'], name_key='y')
        final_dict.update(result_dict)
        #final_dict.update(error_graphs_data)
        print result_dict
        return final_dict
    if dwm_dict.has_key('month'):
        final_result_dict = {}
        final_productivity = {}
        productivity_list={}
        all_internal_error_accuracy = {}
        all_external_error_accuracy = {}
        for month_key,month_values in dwm_dict.iteritems():
            for month_name,month_dates in month_values.iteritems():
                result_dict = product_total_graph(month_dates, prj_id, center, work_packets)
                if len(result_dict['prod_days_data']) > 0:
                    productivity_list[month_name] = result_dict['volumes_data']['volume_values']
                packet_sum_data = result_dict['volumes_data']['volume_values']
                error_graphs_data = internal_extrnal_graphs(request, month_dates, prj_id, center, packet_sum_data)
                for vol_key, vol_values in error_graphs_data['internal_accuracy_graph'].iteritems():
                    if all_internal_error_accuracy.has_key(vol_key):
                        all_internal_error_accuracy[vol_key].append(vol_values)
                    else:
                        all_internal_error_accuracy[vol_key] = [vol_values]
                if error_graphs_data.has_key('external_accuracy_graph'):
                    for vol_key, vol_values in error_graphs_data['external_accuracy_graph'].iteritems():
                        if all_internal_error_accuracy.has_key(vol_key):
                            all_internal_error_accuracy[vol_key].append(vol_values)
                        else:
                            all_internal_error_accuracy[vol_key] = [vol_values]
                if error_graphs_data.has_key('extr_err_accuracy'):
                    for vol_key, vol_values in error_graphs_data['extr_err_accuracy']['packets_percntage'].iteritems():
                        print error_graphs_data['extr_err_accuracy']['packets_percntage']
                        if all_external_error_accuracy.has_key(vol_key):
                            all_external_error_accuracy[vol_key].append(vol_values[0])
                        else:
                            all_external_error_accuracy[vol_key] = vol_values
                print error_graphs_data
        #below for productivity,packet wise performance
        for prodct_key,prodct_value in productivity_list.iteritems():
            for vol_key,vol_values in prodct_value.iteritems():
                if final_productivity.has_key(vol_key):
                    final_productivity[vol_key].update(vol_values)
                else:
                    final_productivity[vol_key]=[vol_values]
        error_volume_data = {}
        volume_new_data = []
        for key, value in final_productivity.iteritems():
            error_graph = []
            error_volume_data[key] = sum(value)
            error_graph.append(key.replace('NA_','').replace('_NA',''))
            error_graph.append(sum(value))
            volume_new_data.append(error_graph)
        result_dict['productivity_data']= graph_data_alignment(final_productivity,name_key='data')
        result_dict['volumes_data']={}
        result_dict['volumes_data']['volume_new_data']= volume_new_data
        for error_key,error_value in all_internal_error_accuracy.iteritems():
            all_internal_error_accuracy[error_key]= sum(error_value)/len(error_value)
            print sum(error_value),len(error_value)
        for error_key,error_value in all_external_error_accuracy.iteritems():
            print error_value
            all_external_error_accuracy[error_key]= sum(error_value)/len(error_value)
            print sum(error_value),len(error_value)
        result_dict['internal_accuracy_graph'] = graph_data_alignment(all_internal_error_accuracy, name_key='y')
        result_dict['external_accuracy_graph'] = graph_data_alignment(all_external_error_accuracy, name_key='y')
        result_dict['data']['date'] = [productivity_list.keys()]
        return result_dict

    if dwm_dict.has_key('week'):
        final_result_dict = {}
        final_productivity = {}
        productivity_list = {}
        all_internal_error_accuracy = {}
        all_external_error_accuracy = {}
        data_date = []
        week_num = 0
        for week_key, week_dates in dwm_dict.iteritems():
            for week in week_dates:
                data_date.append(week[0])
                result_dict = product_total_graph(week, prj_id, center, work_packets)
                if len(result_dict['prod_days_data']) > 0:
                    week_name = str('week' + str(week_num))
                    productivity_list[week_name] = result_dict['volumes_data']['volume_values']
                    week_num = week_num + 1
                packet_sum_data = result_dict['volumes_data']['volume_values']
                error_graphs_data = internal_extrnal_graphs(request, week, prj_id, center, packet_sum_data)
                for vol_key, vol_values in error_graphs_data['internal_accuracy_graph'].iteritems():
                    if all_internal_error_accuracy.has_key(vol_key):
                        all_internal_error_accuracy[vol_key].append(vol_values)
                    else:
                        all_internal_error_accuracy[vol_key] = [vol_values]
                if error_graphs_data.has_key('external_accuracy_graph'):
                    for vol_key, vol_values in error_graphs_data['external_accuracy_graph'].iteritems():
                        if all_internal_error_accuracy.has_key(vol_key):
                            all_internal_error_accuracy[vol_key].append(vol_values)
                        else:
                            all_internal_error_accuracy[vol_key] = [vol_values]
                if error_graphs_data.has_key('extr_err_accuracy'):
                    for vol_key, vol_values in error_graphs_data['extr_err_accuracy']['packets_percntage'].iteritems():
                        print error_graphs_data['extr_err_accuracy']['packets_percntage']
                        if all_external_error_accuracy.has_key(vol_key):
                            all_external_error_accuracy[vol_key].append(vol_values[0])
                        else:
                            all_external_error_accuracy[vol_key] = vol_values
                print error_graphs_data
        # below for productivity,packet wise performance
        for prodct_key, prodct_value in productivity_list.iteritems():
            for vol_key, vol_values in prodct_value.iteritems():
                if final_productivity.has_key(vol_key):
                    final_productivity[vol_key].append(vol_values)
                else:
                    final_productivity[vol_key] = [vol_values]
        error_volume_data = {}
        volume_new_data = []
        for key, value in final_productivity.iteritems():
            error_graph = []
            error_volume_data[key] = sum(value)
            error_graph.append(key.replace('NA_','').replace('_NA',''))
            error_graph.append(sum(value))
            volume_new_data.append(error_graph)
        result_dict['productivity_data'] = graph_data_alignment(final_productivity, name_key='data')
        result_dict['volumes_data'] = {}
        result_dict['volumes_data']['volume_new_data'] = volume_new_data
        for error_key, error_value in all_internal_error_accuracy.iteritems():
            all_internal_error_accuracy[error_key] = sum(error_value) / len(error_value)
            print sum(error_value), len(error_value)
        for error_key, error_value in all_external_error_accuracy.iteritems():
            print error_value
            all_external_error_accuracy[error_key] = sum(error_value) / len(error_value)
            print sum(error_value), len(error_value)
        result_dict['internal_accuracy_graph'] = graph_data_alignment(all_internal_error_accuracy, name_key='y')
        result_dict['external_accuracy_graph'] = graph_data_alignment(all_external_error_accuracy, name_key='y')
        result_dict['data']['date']=data_date
        return result_dict




    #pass
def num_of_days(to_date,from_date):
    date_list=[]
    no_of_days = to_date - from_date
    no_of_days = int(re.findall('\d+', str(no_of_days))[0])
    for i in range(0, no_of_days + 1):
        date_list.append(str(from_date + timedelta(days=i)))
    return date_list
def from_to(request):
    from_date = datetime.datetime.strptime(request.GET['from'],'%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(request.GET['to'],'%Y-%m-%d').date()
    type = request.GET['type']
    #type='day'
    try:
        work_packets = request.GET.get('pack_list').split(',')
    except:
        work_packets = ['DataDownload', 'DetailFinancial']
    project = request.GET['project'].split('-')[0].strip()
    center_id = request.GET['center'].split('-')[0].strip()
    #center = request.GET['center'].split('-')[0].strip()
    #project = 'Probe'
    #center_id = 'Salem'
    date_list = []
    if type == 'day':
        date_list=num_of_days(to_date,from_date)
    if type == 'month':
        months_dict = {}
        days = (to_date - from_date).days
        for i in range(0, days):
            date = from_date + datetime.timedelta(i)
            month = date.strftime("%B")
            if month in months_dict:
                months_dict[month].append(str(date))
            else:
                months_dict[month] = [str(date)]
    if type == 'week':
        months_dict = {}
        days = (to_date - from_date).days
        for i in range(0, days):
            date = from_date + datetime.timedelta(i)
            month = date.strftime("%B")
            if month in months_dict:
                months_dict[month].append(str(date))
            else:
                months_dict[month] = [str(date)]
        weeks = []
        weekdays = []
        if months_dict == {}:
            num_days = to_date.day
            start = 1
            end = 7 - from_date.weekday()
            while start <= num_days:
                weeks.append({'start': start, 'end': end})
                sdate = from_date + datetime.timedelta(start - 1)
                edate = from_date + datetime.timedelta(end - 1)
                weekdays.append({'start': sdate, 'end': edate})
                start = end + 1
                end = end + 7
                if end > num_days:
                    end = num_days
        for key, valu in months_dict.iteritems():
            one_month = months_dict[key]
            fro_mon = datetime.datetime.strptime(one_month[0], '%Y-%m-%d').date()
            to_mon = datetime.datetime.strptime(one_month[-1:][0], '%Y-%m-%d').date()
            no_of_days = to_mon- fro_mon
            num_days = int(re.findall('\d+', str(no_of_days))[0])+1
            #num_days = 4
            start = 1
            end = 7 - fro_mon.weekday()
            while start <= num_days:
                weeks.append({'start': start, 'end': end})
                sdate = fro_mon + datetime.timedelta(start - 1)
                edate = fro_mon + datetime.timedelta(end - 1)
                weekdays.append({'start': sdate, 'end': edate})
                start = end + 1
                end = end + 7
                if end > num_days:
                    end = num_days
        week_list=[]
        for w_days in weekdays:
            date_list = num_of_days(w_days['end'],w_days['start'])
            week_list.append(date_list)
        print week_list
        #week_list=[['2016-09-09', '2016-09-10', '2016-09-11'], ['2016-09-12', '2016-09-13', '2016-09-14', '2016-09-15', '2016-09-16', '2016-09-17', '2016-09-18']]
    dwm_dict= {}
    if type == 'day':
        dwm_dict['day']= date_list
    if type == 'month':
        dwm_dict['month'] = months_dict
    if type == 'week':
        dwm_dict['week'] = week_list
    resul_data = {}
    center = Center.objects.filter(name=center_id).values_list('id', flat=True)
    prj_id = Project.objects.filter(name=project).values_list('id',flat=True)
    final_result_dict = day_week_month(request,dwm_dict,prj_id,center,work_packets)

    return HttpResponse(final_result_dict)
    #below varaibles for productivity,wpf graphs



def chart_data(request):
    to_date = datetime.datetime.strptime(request.GET['date'], '%Y-%m-%d').date()
    work_packet = str(request.GET['packet'])
    packet_dict = {}
    emp_name = RawTable.objects.filter(date=to_date,volume_type=work_packet).values_list('employee',flat=True)
    packet_values = RawTable.objects.filter(date=to_date,volume_type=work_packet).values_list('per_day',flat=True)
    emp_names= [x.encode('UTF8') for x in emp_name]
    work_packet_values = [int(x) for x in packet_values]

    final_data=[]
    packet_dict['emp_names']=emp_names
    packet_dict['work_packet_values'] = work_packet_values
    for emp,packet in zip(emp_names,work_packet_values):
        emp_packet = {}
        emp_packet['emp']=emp
        emp_packet['packet_value']= packet
        final_data.append(emp_packet)
    return HttpResponse(final_data)

def yesterdays_data(request):
    yesterday = date.today() - timedelta(1)
    print yesterday
    date_list = []
    date_list.append(str(yesterday))
    conn = redis.Redis(host="localhost", port=6379, db=0)
    #below varaibles for productivity,wpf graphs
    result = {}
    volumes_dict = {}
    date_values = {}
    volume_list = RawTable.objects.values_list('volume_type', flat=True).distinct()
    distinct_volumes = [x.encode('UTF8') for x in volume_list]
    for date_va in date_list:
        #below code for product,wpf graphs
        for vol_type in volume_list:
            date_pattern = '*{0}_{1}'.format(vol_type,date_va)
            key_list = conn.keys(pattern=date_pattern)
            if not key_list:
                if date_values.has_key(vol_type):
                    date_values[vol_type].append(0)
                else:
                    date_values[vol_type] = [0]
            for cur_key in key_list:
                var = conn.hgetall(cur_key)
                for key,value in var.iteritems():
                    if date_values.has_key(key):
                        date_values[key].append(int(value))
                    else:
                        date_values[key]=[int(value)]
                volumes_dict['data'] = date_values
                volumes_dict['date'] = date_list
                result['data'] = volumes_dict
    #below code for productivity,wpf graph
    volumes_data = result['data']['data']
    volume_bar_data = {}
    volume_bar_data['volume_type']= volumes_data.keys()
    volume_keys_data ={}
    for key,value in volumes_data.iteritems():
        volume_keys_data[key]= sum(value)
    for vol in distinct_volumes:
        if vol not in volume_keys_data and "DetailFinancial" not in vol:
            volume_keys_data[vol]=0
    volume_bar_data['volume_values'] = volume_keys_data
    result['volumes_data'] = volume_bar_data
    print result
    return HttpResponse(result)

