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
from django.db.models import Max
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



def redis_insertion_final(prj_obj,center_obj,dates_list,key_type,level_structure):
    data_dict = {}
    prj_name = prj_obj.name
    center_name = center_obj.name
    all_dates = []
    if key_type == 'Production':
        volumes_list = RawTable.objects.filter(project=prj_obj, center=center_obj).values('sub_project', 'work_packet', 'sub_packet').distinct()
    if key_type == 'Internal':
        volumes_list = Internalerrors.objects.filter(project=prj_obj, center=center_obj).values('sub_project', 'work_packet', 'sub_packet').distinct()
    if key_type == 'External':
        volumes_list = Externalerrors.objects.filter(project=prj_obj, center=center_obj).values('sub_project', 'work_packet', 'sub_packet').distinct()
    for date in dates_list:
        date_is = datetime.datetime.strptime(date,'%Y-%m-%d').date()
        for row_record_dict in volumes_list:
            final_work_packet = ''
            single_row_dict = {}
            query_set = {}
            query_set['date'] = date
            query_set['project'] = prj_obj
            query_set['center'] = center_obj
            #for vol_key, vol_value in row_record_dict.iteritems():
            if 'sub_project' in level_structure:
                final_work_packet = row_record_dict['sub_project']
                query_set['sub_project'] = row_record_dict['sub_project']
            if 'work_packet' in level_structure:
                query_set['work_packet'] = row_record_dict['work_packet']
                if final_work_packet:
                    final_work_packet = final_work_packet + '_' + row_record_dict['work_packet']
                else:
                    final_work_packet = row_record_dict['work_packet']
            if 'sub_packet' in level_structure:
                query_set['sub_packet'] = row_record_dict['sub_packet']
                if final_work_packet:
                    final_work_packet = final_work_packet + '_' + row_record_dict['sub_packet']
                else:
                    final_work_packet = row_record_dict['sub_packet']
            value_dict = {}
            if key_type == 'Production':
                redis_key = '{0}_{1}_{2}_{3}'.format(prj_name,center_name,final_work_packet,str(date_is))
                total = RawTable.objects.filter(**query_set).values_list('per_day').aggregate(Sum('per_day'))
                value_dict[str(final_work_packet)] = str(total['per_day__sum'])
                print value_dict,redis_key
                data_dict[redis_key] = value_dict
            if key_type == 'Internal':
                redis_key = '{0}_{1}_{2}_{3}_error'.format(prj_name,center_name,final_work_packet,str(date_is))
                total_audit = Internalerrors.objects.filter(**query_set).values_list('audited_errors').aggregate(Sum('audited_errors'))
                total_errors = Internalerrors.objects.filter(**query_set).values_list('total_errors').aggregate(Sum('total_errors'))
                value_dict['total_audit'] = str(total_audit['audited_errors__sum'])
                value_dict['total_errors'] = str(total_errors['total_errors__sum'])
                print value_dict,redis_key
                data_dict[redis_key] = value_dict
            if key_type == 'External':
                redis_key = '{0}_{1}_{2}_{3}_externalerror'.format(prj_name,center_name,final_work_packet,str(date_is))
                total_audit = Externalerrors.objects.filter(**query_set).values_list('audited_errors').aggregate(Sum('audited_errors'))
                total_errors = Externalerrors.objects.filter(**query_set).values_list('total_errors').aggregate(Sum('total_errors'))
                value_dict['total_audit'] = str(total_audit['audited_errors__sum'])
                value_dict['total_errors'] = str(total_errors['total_errors__sum'])
                print value_dict,redis_key
                data_dict[redis_key] = value_dict

    print data_dict, all_dates
    conn = redis.Redis(host="localhost", port=6379, db=0)
    current_keys = []
    for key, value in data_dict.iteritems():
        current_keys.append(key)
        conn.hmset(key, value)
    return "hai"


def redis_insert(prj_obj,center_obj,dates_list,key_type):
    wp_count,sub_pct_count,sub_prj_count = 0,0,0
    level_herarchy = []
    wk_packet , wk_packet , sub_prj = [],[],[]
    if key_type == 'Production':
        level_herarchy_packets = RawTable.objects.filter(project=prj_obj, center=center_obj).values('sub_project','work_packet','sub_packet').distinct()
        wk_packet = [wp_count+1 for key in level_herarchy_packets if len(key['work_packet'])]
        sub_packet = [sub_pct_count+1 for key in level_herarchy_packets if len(key['sub_packet'])]
        sub_prj = [sub_prj_count+1 for key in level_herarchy_packets if len(key['sub_project'])]
    if key_type == 'Internal':
        level_herarchy_packets = Internalerrors.objects.filter(project=prj_obj, center=center_obj).values('sub_project', 'work_packet', 'sub_packet').distinct()
        wk_packet = [wp_count + 1 for key in level_herarchy_packets if len(key['work_packet'])]
        sub_packet = [sub_pct_count + 1 for key in level_herarchy_packets if len(key['sub_packet'])]
        sub_prj = [sub_prj_count + 1 for key in level_herarchy_packets if len(key['sub_project'])]
    if key_type == 'External':
        level_herarchy_packets = Externalerrors.objects.filter(project=prj_obj, center=center_obj).values('sub_project', 'work_packet', 'sub_packet').distinct()
        wk_packet = [wp_count + 1 for key in level_herarchy_packets if len(key['work_packet'])]
        sub_packet = [sub_pct_count + 1 for key in level_herarchy_packets if len(key['sub_packet'])]
        sub_prj = [sub_prj_count + 1 for key in level_herarchy_packets if len(key['sub_project'])]
    if len(wk_packet) > 0 : level_herarchy.append('work_packet')
    if len(sub_packet) > 0: level_herarchy.append('sub_packet')
    if len(sub_prj) > 0: level_herarchy.append('sub_project')

    level_dict ={}
    if len(level_herarchy)  == 3:
        level_dict['level3'] = ['sub_projecct','work_packet','sub_packet']
        level_dict['level2'] = ['sub_projecct','work_packet']
        level_dict['level1'] = ['sub_projecct']
    if len(level_herarchy)  == 2:
        if 'sub_project' in level_herarchy:
            level_dict['level2'] = ['sub_project','work_packet']
            level_dict['level1'] = ['sub_projecct']
        else :
            level_dict['level2'] = ['work_packet','sub_packet']
            level_dict['level1'] = ['work_packet']
    if len(level_herarchy) == 1:
        level_dict['level1'] = level_dict['level1'] = ['work_packet']
    for level_key in level_dict:
        final_inserting = redis_insertion_final(prj_obj, center_obj, dates_list, key_type, level_dict[level_key])
    return "completed"



def redis_insert_old(prj_obj,center_obj,dates_list,key_type):
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
            volumes_list = RawTable.objects.filter(project=prj_obj,center=center_obj,date=date ).values('sub_project','work_packet','sub_packet','date').distinct()
        if key_type == 'Internal':
            volumes_list = Internalerrors.objects.filter(project=prj_obj,center=center_obj, date=date).values('sub_project','work_packet','sub_packet', 'date').distinct()
        if key_type == 'External':
            volumes_list = Externalerrors.objects.filter(project=prj_obj, center=center_obj, date=date).values('sub_project', 'work_packet', 'sub_packet', 'date').distinct()
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
                print value_dict
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
                print value_dict
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
                print value_dict
                data_dict[redis_key] = value_dict

    print data_dict,all_dates
    conn = redis.Redis(host="localhost", port=6379, db=0)
    current_keys = []
    for key,value in data_dict.iteritems():
        current_keys.append(key)
        conn.hmset(key,value)
    return "hai"



def raw_table_query_insertion(customer_data,prj_obj,center_obj,teamleader_obj_name,per_day_value,db_check):
    print customer_data
    prod_date_list = customer_data['date']
    new_can = 0
    check_query = RawTable.objects.filter(project=prj_obj, sub_project=customer_data.get('sub_project', ''),
                                          work_packet=customer_data['work_packet'],
                                          sub_packet=customer_data.get('sub_packet', ''),
                                          employee_id=customer_data.get('emp_id', ''), date=customer_data['date'],
                                          center=center_obj).values('per_day','id')
    if len(check_query) == 0:
        new_can = RawTable(project=prj_obj, sub_project=customer_data.get('sub_project', ''),
                           work_packet=customer_data['work_packet'],
                           sub_packet=customer_data.get('sub_packet', ''),
                           employee_id=customer_data.get('emp_id', ''),
                           per_hour=0,
                           per_day=per_day_value, date=customer_data['date'],
                           norm=int(float(customer_data['target'])),
                           team_lead=teamleader_obj_name, center=center_obj)
        if new_can:
            try:
                print customer_data
                new_can.save()
            except:
                print "error in raw_table_query"
    if len(check_query) > 0:
        #import pdb;pdb.set_trace()
        if db_check == 'aggregate':
            per_day_value = per_day_value + int(check_query[0]['per_day'])
            new_can_agr = RawTable.objects.filter(id=int(check_query[0]['id'])).update(per_day=per_day_value)
        elif db_check == 'update':
            new_can_upd = RawTable.objects.filter(id=int(check_query[0]['id'])).update(per_day=per_day_value)

    return prod_date_list

def internalerror_query_insertion(customer_data, prj_obj, center_obj,teamleader_obj_name, audited_count,total_errors, db_check):
    internal_date_list = customer_data['date']
    check_query = Internalerrors.objects.filter(project=prj_obj, sub_project=customer_data.get('sub_project', ''),
                                          work_packet=customer_data['work_packet'],
                                          sub_packet=customer_data.get('sub_packet', ''),
                                          employee_id=customer_data.get('emp_id', ''),date=customer_data['date'],
                                          center=center_obj).values('audited_errors','total_errors', 'id')
    if len(check_query) == 0:
        new_can = Internalerrors(employee_id=customer_data.get('emp_id', ''),
                                 sub_project=customer_data.get('sub_project', ''),
                                 work_packet=customer_data['work_packet'],
                                 sub_packet=customer_data.get('sub_packet', ''), date=customer_data['date'],
                                 audited_errors=int(float(audited_count)),
                                 total_errors=total_errors,
                                 project=prj_obj, center=center_obj, error_name=customer_data.get('error_name', ''))
        if new_can:
            try:
                print customer_data
                new_can.save()
            except:
                print "error in internal_table_query"

    if len(check_query) > 0:
        if db_check == 'aggregate':
            audited_count = audited_count + int(check_query[0]['audited_errors'])
            total_errors = total_errors + int(check_query[0]['total_errors'])
            new_can_agr = Internalerrors.objects.filter(id=int(check_query[0]['id'])).update(audited_errors=audited_count,total_errors=total_errors)
        elif db_check == 'update':
            new_can_upd = Internalerrors.objects.filter(id=int(check_query[0]['id'])).update(audited_errors=audited_count,total_errors=total_errors)
    return internal_date_list

def externalerror_query_insertion(customer_data, prj_obj, center_obj,teamleader_obj_name, audited_count,total_errors, db_check):
    external_date_list = customer_data['date']
    new_can = 0
    check_query = Externalerrors.objects.filter(project=prj_obj, sub_project=customer_data.get('sub_project', ''),
                                          work_packet=customer_data['work_packet'],
                                          sub_packet=customer_data.get('sub_packet', ''),
                                          employee_id=customer_data.get('emp_id', ''),date=customer_data['date'],
                                          center=center_obj).values('audited_errors','total_errors', 'id')
    if len(check_query) == 0:
        new_can = Externalerrors(employee_id=customer_data.get('emp_id', ''),
                                 sub_project=customer_data.get('sub_project', ''),
                                 work_packet=customer_data['work_packet'],
                                 sub_packet=customer_data.get('sub_packet', ''), date=customer_data['date'],
                                 audited_errors=int(float(audited_count)),
                                 total_errors=total_errors,
                                 project=prj_obj, center=center_obj, error_name=customer_data.get('error_name', ''))
        if new_can:
            try:
                print customer_data
                new_can.save()
            except:
                print "error in external_table_query"
    if len(check_query) > 0:
        print customer_data
        if db_check == 'aggregate':
            audited_count = audited_count + int(check_query[0]['audited_errors'])
            total_errors = total_errors + int(check_query[0]['total_errors'])
            new_can_agr = Externalerrors.objects.filter(id=int(check_query[0]['id'])).update(audited_errors=audited_count,total_errors=total_errors)
        elif db_check == 'update':
            new_can_update = Externalerrors.objects.filter(id=int(check_query[0]['id'])).update(audited_errors=audited_count,total_errors=total_errors)

    return external_date_list


def upload(request):
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
        project_type = Project.objects.filter(name=prj_obj.name,center=center_obj).values_list('project_type',flat=True)
        if len(project_type)>0:
            project_type = str(project_type[0])
        db_check = str(Project.objects.filter(name=prj_obj.name,center=center_obj).values_list('project_db_handling',flat=True)[0])
        sheet_count = Authoringtable.objects.filter(project=prj_obj, center=center_obj).values_list('sheet_name',flat=True).distinct()
        for key,value in sheet_index_dict.iteritems():
            one_sheet_data = {}
            prod_date_list,internal_date_list,external_date_list=[],[],[]
            open_sheet = open_book.sheet_by_index(value)
            SOH_XL_HEADERS = open_sheet.row_values(0)
            main_headers = Authoringtable.objects.filter(sheet_name=key,project=prj_obj,center=center_obj).values_list('sheet_field',flat=True)
            sheet_main_headers = main_headers
            table_schema = Authoringtable.objects.filter(sheet_name=key,project=prj_obj,center=center_obj).values_list('table_schema',flat=True)
            table_name = Authoringtable.objects.filter(sheet_name=key,project=prj_obj,center=center_obj).values_list('table_type',flat=True).distinct()
            if len(table_name) > 0 :
                table_name = str(table_name[0])
            mapping_table = {}
            for sh_filed,t_field in zip(sheet_main_headers,table_schema):
                mapping_table[sh_filed] = t_field
            SOH_XL_MAN_HEADERS = [x.title() for x in main_headers]
            sheet_headers = validate_sheet(open_sheet,request,SOH_XL_HEADERS,SOH_XL_MAN_HEADERS)
            for row_idx in range(1, open_sheet.nrows):
                error_type = {}
                raw_sheet_data = {}
                customer_data = {}
                for column, col_idx in sheet_headers:
                    cell_data = get_cell_data(open_sheet, row_idx, col_idx)
                    column_name = mapping_table.get(column, '')
                    if column in ["date", "from date","to date","audited date"]:
                        cell_data = xlrd.xldate_as_tuple(int(cell_data.split('.')[0]), 0)
                        cell_data = '%s-%s-%s' % (cell_data[0], cell_data[1], cell_data[2])
                        customer_data[column_name] = ''.join(cell_data)
                        raw_sheet_data[column_name] = ''.join(cell_data)
                    elif column !="date," and column in mapping_table.keys():
                        customer_data[column_name] = ''.join(cell_data)
                        raw_sheet_data[column_name] = ''.join(cell_data)

                if prj_name in ['Dellcoding']:
                    if raw_sheet_data['date'] not in one_sheet_data.keys():
                        one_sheet_data[raw_sheet_data['date']]=[raw_sheet_data]
                    else:
                        one_sheet_data[raw_sheet_data['date']].append(raw_sheet_data)
                    if row_idx == (open_sheet.nrows-1):
                        one_sheet = sheet_upload_one(prj_obj, center_obj, teamleader_obj_name, key, one_sheet_data)

                if len(sheet_count) >= 3 :
                    if table_name == 'raw_table':
                        if customer_data.has_key('target') == False:
                            customer_data['target'] = 0
                        try:
                            per_day_value = int(float(customer_data.get('work_done', '')))
                        except:
                            per_day_value = 0
                        raw_table_insert = raw_table_query_insertion(customer_data,prj_obj,center_obj,teamleader_obj_name,per_day_value,db_check)
                        prod_date_list.append(customer_data['date'])
                    if table_name == 'internal_error':
                        try:
                            total_errors = int(float(customer_data['total_errors']))
                        except:
                            total_errors = 0
                        if customer_data.has_key('audited_count') == False:
                            audited_count = 0
                        if customer_data.get('audited_count', '') :
                            audited_count = customer_data.get('audited_count', '')
                        internalerror_insert = internalerror_query_insertion(customer_data, prj_obj, center_obj,teamleader_obj_name, audited_count,total_errors, db_check)
                        internal_date_list.append(customer_data['date'])
                    if table_name == 'external_error':
                        try:
                            total_errors = int(float(customer_data['total_errors']))
                        except:
                            total_errors = 0
                        if customer_data.has_key('audited_count') == False:
                            audited_count = 0
                        if customer_data.get('audited_count', '') :
                            audited_count = customer_data.get('audited_count', '')
                        externalerror_insert = externalerror_query_insertion(customer_data, prj_obj, center_obj,teamleader_obj_name, audited_count,total_errors, db_check)
                        external_date_list.append(customer_data['date'])

                if len(sheet_count) == 2 :
                    if table_name == 'raw_table':
                        if customer_data.has_key('target') == False:
                            customer_data['target'] = 0
                        try:
                            per_day_value = int(float(customer_data.get('work_done', '')))
                        except:
                            per_day_value = 0
                        raw_table_insert = raw_table_query_insertion(customer_data,prj_obj,center_obj,teamleader_obj_name,per_day_value,db_check)
                        prod_date_list.append(customer_data['date'])
                    if table_name == 'internal_external' and customer_data.get('error_type','')== 'Internal':
                        if customer_data.get('audited_count','') :
                            audited_count = customer_data.get('audited_count','')
                        else:
                            try:
                                audited_count = int(float(customer_data['qced_count']))
                            except:
                                audited_count = 0
                        try:
                            total_errors = int(float(customer_data['total_errors']))
                        except:
                            total_errors = 0
                        internalerror_insert = internalerror_query_insertion(customer_data, prj_obj, center_obj,teamleader_obj_name, audited_count,total_errors, db_check)
                        internal_date_list.append(customer_data['date'])
                    if table_name == 'internal_external' and customer_data.get('error_type','')== 'External':
                        if customer_data.get('audited_count','') :
                            audited_count = customer_data.get('audited_count','')
                        else:
                            try:
                                    audited_count = int(float(customer_data['daily_audit']))
                            except:
                                audited_count = 0
                        try:
                            total_errors = int(float(customer_data['total_errors']))
                        except:
                            total_errors = 0
                        externalerror_insert = externalerror_query_insertion(customer_data, prj_obj, center_obj,teamleader_obj_name, audited_count,total_errors, db_check)
                        external_date_list.append(customer_data['date'])


            if len(sheet_count) >= 3:
                if table_name == 'raw_table':
                    prod_date_list =list(set(prod_date_list))
                    insert = redis_insert(prj_obj, center_obj, prod_date_list, key_type='Production')
                if table_name == 'internal_error':
                    internal_date_list = list(set(internal_date_list))
                    insert = redis_insert(prj_obj, center_obj, internal_date_list, key_type='Internal')
                if table_name == 'external_error':
                    external_date_list = list(set(external_date_list))
                    insert = redis_insert(prj_obj, center_obj, external_date_list, key_type='External', )

            if len(sheet_count) == 2:
                prod_date_list = list(set(prod_date_list))
                if table_name == 'raw_table':
                    insert = redis_insert(prj_obj, center_obj, prod_date_list, key_type='Production')
                if table_name == 'internal_external':
                    external_date_list = list(set(external_date_list))
                    internal_date_list = list(set(internal_date_list))
                    insert = redis_insert(prj_obj, center_obj, external_date_list, key_type='External')
                    insert = redis_insert(prj_obj, center_obj, internal_date_list, key_type='Internal')

            var ='hello'
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



def level_hierarchy_key(level_structure_key,vol_type):
    final_work_packet = ''

    if level_structure_key.has_key('sub_project'):
        if vol_type['sub_project'] !='':
            final_work_packet = vol_type['sub_project']
    if level_structure_key.has_key('work_packet'):
        if final_work_packet and vol_type['work_packet'] != '':
            final_work_packet = final_work_packet + '_' + vol_type['work_packet']
        else:
            if vol_type['work_packet'] != '':
                final_work_packet = vol_type['work_packet']
    if level_structure_key.has_key('sub_packet'):
        if final_work_packet and vol_type['sub_packet'] != '':
            final_work_packet = final_work_packet + '_' + vol_type['sub_packet']
        else:
            if vol_type['sub_packet'] != '':
                final_work_packet = vol_type['sub_packet']
    return  final_work_packet

def query_set_generation(prj_id,center_obj,level_structure_key):
    query_set = {}
    query_set['project'] = prj_id
    query_set['center'] = center_obj
    if level_structure_key.has_key('sub_project'):
        query_set['sub_project'] = level_structure_key['sub_project']
    if level_structure_key.has_key('work_packet'):
        query_set['work_packet'] = level_structure_key['work_packet']
    if level_structure_key.has_key('sub_packet'):
        query_set['sub_packet'] = level_structure_key['sub_packet']
    return query_set

def product_total_graph(date_list,prj_id,center_obj,work_packets,level_structure_key):
    work = work_packets
    conn = redis.Redis(host="localhost", port=6379, db=0)
    result = {}
    volumes_dict = {}
    date_values = {}
    #volume_list = RawTable.objects.filter(project=prj_id,center=center_obj).values_list('volume_type', flat=True).distinct()
    prj_name = Project.objects.filter(id=prj_id).values_list('name',flat=True)
    center_name = Center.objects.filter(id=center_obj).values_list('name', flat=True)
    query_set = query_set_generation(prj_id,center_obj,level_structure_key)
    for date_va in date_list:
        #below code for product,wpf graphs
        if level_structure_key.has_key('work_packet') and len(level_structure_key) ==1:
            volume_list = RawTable.objects.filter(**query_set).values('sub_project','work_packet').distinct()
        else:
            volume_list = RawTable.objects.filter(**query_set).values('sub_project','work_packet','sub_packet').distinct()
        count =0
        for vol_type in volume_list:
            final_work_packet = level_hierarchy_key(level_structure_key,vol_type)
            if not final_work_packet:
                final_work_packet = level_hierarchy_key(volume_list[count],vol_type)
            count = count+1
            date_pattern = '{0}_{1}_{2}_{3}'.format(prj_name[0], str(center_name[0]), str(final_work_packet), date_va)
            key_list = conn.keys(pattern=date_pattern)
            if not key_list:
                if date_values.has_key(final_work_packet):
                    date_values[final_work_packet].append(0)
                else:
                    date_values[final_work_packet] = [0]
            for cur_key in key_list:
                var = conn.hgetall(cur_key)
                for key,value in var.iteritems():
                    if value == 'None':
                        value = 0
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
    if None in volumes_data.keys():
        del volumes_data[None]
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
        try:
            if 'DetailFinancial' not in key:
                if volume_dict.has_key(key):
                    new_list.append(volume_dict[key])
                else:
                    new_list.append(key)
                new_list.append(value)
                volume_list_data.append(new_list)
        except:
            import pdb;pdb.set_trace()
    volume_bar_data['volume_new_data']=volume_list_data
    volume_bar_data['volume_values'] = volume_keys_data
    result['volumes_data'] = volume_bar_data
    print result
    return result



def internal_extrnal_graphs_same_formula(request,date_list,prj_id,center_obj,level_structure_key,err_type):
    prj_name = Project.objects.filter(id=prj_id).values_list('name', flat=True)
    center_name = Center.objects.filter(id=center_obj).values_list('name', flat=True)
    query_set = query_set_generation(prj_id, center_obj, level_structure_key)
    if err_type =='Internal' :
        extr_volumes_list = Internalerrors.objects.filter(**query_set).values('sub_project','work_packet','sub_packet').distinct()
        err_key_type = 'error'
    if err_type == 'External':
        extr_volumes_list = Externalerrors.objects.filter(**query_set).values('sub_project','work_packet','sub_packet').distinct()
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
        count =0
        for vol_type in extr_volumes_list:
            """for vol_keys, vol_values in vol_type.iteritems():
                if vol_values == '':
                    vol_type[vol_keys] = 'NA'
            work_packets = vol_type['sub_project'] + '_' + vol_type['work_packet'] + '_' + vol_type['sub_packet']"""
            #work_packets = vol_type['work_packet']
            final_work_packet = level_hierarchy_key(level_structure_key, vol_type)
            if not final_work_packet:
                final_work_packet = level_hierarchy_key(extr_volumes_list[count],vol_type)
            count = count+1
            extr_volumes_list_new.append(final_work_packet)
            key_pattern = '{0}_{1}_{2}_{3}_{4}'.format(prj_name[0], str(center_name[0]), final_work_packet, date_va,err_key_type)
            audit_key_list = conn.keys(pattern=key_pattern)
            if not audit_key_list:
                if vol_error_values.has_key(final_work_packet):
                    vol_error_values[final_work_packet].append(0)
                    vol_audit_data[final_work_packet].append(0)
                else:
                    vol_error_values[final_work_packet] = [0]
                    vol_audit_data[final_work_packet] = [0]
            for cur_key in audit_key_list:
                var = conn.hgetall(cur_key)
                for key, value in var.iteritems():
                    if value == 'None':
                        value = 0
                    error_vol_type = final_work_packet
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
        if (volume in error_volume_data.keys()) and (volume in error_audit_data.keys()) :
            if error_audit_data[volume] != 0:
                percentage = (float(error_volume_data[volume]) / error_audit_data[volume]) * 100
                percentage = 100 -float('%.2f' % round(percentage, 2))
                error_accuracy[volume] = percentage
            else:
                error_accuracy[volume] = 0
    total_graph_data = {}
    internal_time_line = {}
    for key,value in vol_audit_data.iteritems():
        count =0
        for vol_error_value in value:
            if vol_error_value > 0:
                percentage = (float(vol_error_values[key][count]) / vol_error_value) * 100
                percentage = 100-float('%.2f' % round(percentage, 2))
            else:
                percentage = 0
            if internal_time_line.has_key(key):
                internal_time_line[key].append(percentage)
            else:
                internal_time_line[key] = [percentage]
                internal_time_line[key] = [percentage]
            count= count+1

    range_internal_time_line = {}
    if err_type == 'Internal':
        range_internal_time_line['internal_time_line'] = internal_time_line
        range_internal_time_line['date'] = date_list
        result['internal_error_count'] = error_volume_data
        result['internal_accuracy_graph'] = error_accuracy
        result['internal_time_line'] = range_internal_time_line


    if err_type == 'External':
        range_internal_time_line['external_time_line'] = internal_time_line
        range_internal_time_line['date'] = date_list
        result['external_error_count'] = error_volume_data
        result['external_accuracy_graph'] = error_accuracy
        result['external_time_line'] = range_internal_time_line

    return result

    # below code for external graphs


def externalerror_graph(request,date_list,prj_id,center_obj,packet_sum_data,level_structure_key):
    prj_name = Project.objects.filter(id=prj_id).values_list('name', flat=True)
    center_name = Center.objects.filter(id=center_obj).values_list('name', flat=True)
    query_set = query_set_generation(prj_id, center_obj, level_structure_key)
    extr_volumes_list = Externalerrors.objects.filter(**query_set).values('sub_project','work_packet','sub_packet').distinct()
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
        count =0
        for vol_type in extr_volumes_list:
            final_work_packet = level_hierarchy_key(level_structure_key, vol_type)
            if not final_work_packet:
                final_work_packet = level_hierarchy_key(extr_volumes_list[count], vol_type)
            count = count + 1

            extr_volumes_list_new.append(final_work_packet)
            #extr_key_pattern = '*{0}*_externalerror'.format(date_va)
            extr_key_pattern =  '{0}_{1}_{2}_{3}_externalerror'.format(prj_name[0], str(center_name[0]), final_work_packet, date_va)
            extr_key_list = conn.keys(pattern=extr_key_pattern)
            if not extr_key_list:
                if extrnl_error_values.has_key(final_work_packet):
                    extrnl_error_values[final_work_packet].append(0)
                    extrnl_err_type[final_work_packet].append(0)
                else:
                    extrnl_error_values[final_work_packet] = [0]
                    extrnl_err_type[final_work_packet] = [0]
            for cur_key in extr_key_list:
                var = conn.hgetall(cur_key)
                for key, value in var.iteritems():
                    if value == 'None':
                        value = 0
                    error_vol_type = final_work_packet
                    #import pdb;pdb.set_trace()
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

    date_values = {}
    for date_va in date_list:
        #below code for product,wpf graphs
        volume_list = RawTable.objects.filter(**query_set).values('sub_project','work_packet','sub_packet').distinct()
        count =0
        for vol_type in volume_list:
            final_work_packet = level_hierarchy_key(level_structure_key,vol_type)
            if not final_work_packet:
                final_work_packet = level_hierarchy_key(volume_list[count],vol_type)
            count = count+1
            date_pattern = '{0}_{1}_{2}_{3}'.format(prj_name[0], str(center_name[0]), str(final_work_packet), date_va)
            key_list = conn.keys(pattern=date_pattern)
            if not key_list:
                if date_values.has_key(final_work_packet):
                    date_values[final_work_packet].append(0)
                else:
                    date_values[final_work_packet] = [0]
            for cur_key in key_list:
                var = conn.hgetall(cur_key)
                for key,value in var.iteritems():
                    if value == 'None':
                        value = 0
                    if date_values.has_key(key):
                        date_values[key].append(int(value))
                    else:
                        date_values[key]=[int(value)]

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
    external_time_line = {}
    #import pdb;pdb.set_trace()
    product_data={}
    for key,value in extrnl_err_type.iteritems():
        count =0
        for vol_error_value in value:
            if date_values.has_key(key):
                if date_values[key][count] > 0:
                    percentage = (float(extrnl_error_values[key][count]) / date_values[key][count]) * 100
                    percentage = 100-float('%.2f' % round(percentage, 2))
                else:
                    percentage = 0
                if external_time_line.has_key(key):
                    external_time_line[key].append(percentage)
                else:
                    external_time_line[key] = [percentage]
                    external_time_line[key] = [percentage]
            count= count+1
    range_internal_time_line = {}
    range_internal_time_line['external_time_line'] = external_time_line
    range_internal_time_line['date'] = date_list

    result['extr_err_accuracy'] = {}
    #result['extr_err_accuracy']['packets_percntage'] = graph_data_alignment(extr_err_accuracy, name_key='data')
    result['extr_err_accuracy']['packets_percntage'] = extr_err_accuracy
    result['extr_err_accuracy']['extr_err_name'] = extr_err_acc_name
    result['extr_err_accuracy']['extr_err_perc'] = extr_err_acc_perc
    result['external_time_line'] = range_internal_time_line

    if 'DFES' in extrnl_error_sum:
        del extrnl_error_sum['DFES']
    result['extrn_error_count'] = graph_data_alignment(extrnl_error_sum, name_key='y')
    # print result
    return result


def internal_extrnal_graphs(request,date_list,prj_id,center_obj,packet_sum_data,level_structure_key):
    prj_name = Project.objects.filter(id=prj_id).values_list('name', flat=True)
    center_name = Center.objects.filter(id=center_obj).values_list('name', flat=True)
    final_internal_data = internal_extrnal_graphs_same_formula(request, date_list, prj_id, center_obj,level_structure_key,err_type='Internal')
    if prj_name[0] in ['DellBilling','Dellcoding']:
        final_external_data = internal_extrnal_graphs_same_formula(request, date_list, prj_id, center_obj,level_structure_key,err_type='External')
        final_internal_data.update(final_external_data)
        return final_internal_data
    if prj_name[0] in ['Probe']:
        final_external_data = externalerror_graph(request, date_list, prj_id, center_obj,packet_sum_data,level_structure_key)
        final_internal_data.update(final_external_data)
        return final_internal_data
    result={}
    #return result




def day_week_month(request,dwm_dict,prj_id,center,work_packets,level_structure_key):
    if dwm_dict.has_key('day'):
        final_dict = {}
        result_dict = product_total_graph(dwm_dict['day'],prj_id,center,work_packets,level_structure_key)
        if len(result_dict['prod_days_data'])>0:
            result_dict['productivity_data'] = graph_data_alignment(result_dict['prod_days_data'],name_key='data')
        packet_sum_data = result_dict['volumes_data']['volume_values']
        error_graphs_data = internal_extrnal_graphs(request, dwm_dict['day'], prj_id, center, packet_sum_data,level_structure_key)
        #final_dict['internal_time_line'] = error_graphs_data['internal_time_line']
        if len(error_graphs_data['internal_time_line'])>0:
            final_dict['internal_time_line'] = graph_data_alignment(error_graphs_data['internal_time_line']['internal_time_line'],name_key='data')
        if len(error_graphs_data['external_time_line'])>0:
            final_dict['external_time_line'] = graph_data_alignment(error_graphs_data['external_time_line']['external_time_line'],name_key='data')
        int_value_range= error_graphs_data['internal_accuracy_graph']
        int_min_value,int_max_value = 0,0
        if len(int_value_range)>0:
            if (min(int_value_range.values())>0):
                int_min_value = int(round(min(int_value_range.values()) - 2))
                int_max_value = int(round(max(int_value_range.values()) + 2))
            else:
                int_min_value = int(round(min(int_value_range.values())))
                int_max_value = int(round(max(int_value_range.values()) + 2))
        final_dict['int_min_value'] = int_min_value
        final_dict['int_max_value'] = int_max_value
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
        sub_pro_level = RawTable.objects.filter(project=prj_id, center=center).values_list('sub_project').distinct()
        sub_project_level = [i[0] for i in sub_pro_level]
        if len(sub_project_level) > 1:
            sub_project_level.append('all')
        if len(sub_project_level) <= 1 and sub_project_level[0] == u'' :
            sub_project_level = ''
        work_pac_level = RawTable.objects.filter(project=prj_id, center=center).values_list('work_packet').distinct()
        work_packet_level = [j[0] for j in work_pac_level]
        if len(work_packet_level) > 1:
            work_packet_level.append('all')
        if len(work_packet_level) <= 1 and work_packet_level[0] == u'':
            work_packet_level = ''
        sub_pac_level = RawTable.objects.filter(project=prj_id, center=center).values_list('sub_packet').distinct()
        sub_packet_level = [k[0] for k in sub_pac_level]
        if len(sub_packet_level) > 1:
            sub_packet_level.append('all')
        if len(sub_packet_level) <= 1 and sub_packet_level[0] == u'':
            sub_packet_level = ''
        final_dict['sub_project_level'] = sub_project_level
        final_dict['work_packet_level'] = work_packet_level
        final_dict['sub_packet_level'] = sub_packet_level
        ext_min_value,ext_max_value = 0,0
        if error_graphs_data.has_key('extr_err_accuracy'):
            ext_value_range = error_graphs_data['extr_err_accuracy']['extr_err_perc']
            if len(ext_value_range)>0:
                if ext_value_range != '' and min(ext_value_range)>0:
                    ext_min_value = int(round(min(ext_value_range) - 2))
                    ext_max_value = int(round(max(ext_value_range) + 2))
                else:
                    ext_min_value = int(round(min(ext_value_range)))
                    ext_max_value = int(round(max(ext_value_range) + 2))
            final_dict['ext_min_value'] = ext_min_value
            final_dict['ext_max_value'] = ext_max_value
        #final_dict.update(error_graphs_data)
        print result_dict
        return final_dict
    if dwm_dict.has_key('month'):
        final_result_dict = {}
        final_internal_accuracy_timeline = {}
        internal_accuracy_timeline = {}
        final_external_accuracy_timeline = {}
        external_accuracy_timeline = {}
        #final_external_accuracy_timeline = {}
        final_productivity = {}
        productivity_list={}
        all_internal_error_accuracy = {}
        all_external_error_accuracy = {}
        for month_key,month_values in dwm_dict.iteritems():
            for month_name,month_dates in month_values.iteritems():
                result_dict = product_total_graph(month_dates,prj_id,center,work_packets,level_structure_key)
                if len(result_dict['prod_days_data']) > 0:
                    productivity_list[month_name] = result_dict['volumes_data']['volume_values']
                packet_sum_data = result_dict['volumes_data']['volume_values']

                error_graphs_data = internal_extrnal_graphs(request, month_dates, prj_id, center, packet_sum_data,level_structure_key)
                if len(error_graphs_data['internal_time_line']) > 0:
                    internal_accuracy_timeline[month_name] = error_graphs_data['internal_time_line']['internal_time_line']
                if len(error_graphs_data['external_time_line']) > 0:
                    external_accuracy_timeline[month_name] = error_graphs_data['external_time_line']['external_time_line']

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
        print internal_accuracy_timeline
        for prodct_key,prodct_value in internal_accuracy_timeline.iteritems():
            for vol_key,vol_values in prodct_value.iteritems():
                if final_internal_accuracy_timeline.has_key(vol_key):
                    final_internal_accuracy_timeline[vol_key] = final_internal_accuracy_timeline[vol_key]+vol_values
                else:
                    final_internal_accuracy_timeline[vol_key]=vol_values
        result_dict['internal_accuracy_timeline'] = graph_data_alignment(final_internal_accuracy_timeline, name_key='data')

        for prodct_key,prodct_value in external_accuracy_timeline.iteritems():
            for vol_key,vol_values in prodct_value.iteritems():
                if final_external_accuracy_timeline.has_key(vol_key):
                    final_external_accuracy_timeline[vol_key] = final_external_accuracy_timeline[vol_key]+vol_values
                else:
                    final_external_accuracy_timeline[vol_key]=vol_values
        result_dict['external_accuracy_timeline'] = graph_data_alignment(final_external_accuracy_timeline,name_key='data')
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
        final_internal_accuracy_timeline = {}
        internal_accuracy_timeline = {}
        final_external_accuracy_timeline = {}
        external_accuracy_timeline = {}
        #final_external_accuracy_timeline = {}
        #external_accuracy_timeline = {}
        #final_external_accuracy_timeline = {}
        final_productivity = {}
        productivity_list = {}
        all_internal_error_accuracy = {}
        all_external_error_accuracy = {}
        data_date = []
        week_num = 0
        internal_week_num = 0
        external_week_num = 0
        for week_key, week_dates in dwm_dict.iteritems():
            for week in week_dates:
                data_date.append(week[0])
                result_dict = product_total_graph(week,prj_id,center,work_packets,level_structure_key)
                if len(result_dict['prod_days_data']) > 0:
                    week_name = str('week' + str(week_num))
                    productivity_list[week_name] = result_dict['volumes_data']['volume_values']
                    week_num = week_num + 1
                packet_sum_data = result_dict['volumes_data']['volume_values']
                error_graphs_data = internal_extrnal_graphs(request, week, prj_id, center, packet_sum_data,level_structure_key)
                if len(error_graphs_data['internal_time_line']) > 0:
                    internal_week_name = str('week' + str(internal_week_num))
                    internal_accuracy_timeline[internal_week_name] = error_graphs_data['internal_time_line']['internal_time_line']
                    internal_week_num = internal_week_num + 1

                if len(error_graphs_data['external_time_line']) > 0:
                    external_week_name = str('week' + str(external_week_num))
                    external_accuracy_timeline[external_week_name] = error_graphs_data['external_time_line']['external_time_line']
                    external_week_num = external_week_num + 1
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

        for prodct_key, prodct_value in internal_accuracy_timeline.iteritems():
            for vol_key, vol_values in prodct_value.iteritems():
                if final_internal_accuracy_timeline.has_key(vol_key):
                    final_internal_accuracy_timeline[vol_key] = final_internal_accuracy_timeline[vol_key] + vol_values
                else:
                    final_internal_accuracy_timeline[vol_key] = vol_values
        result_dict['internal_accuracy_timeline'] = graph_data_alignment(final_internal_accuracy_timeline,name_key='data')

        for prodct_key, prodct_value in external_accuracy_timeline.iteritems():
            for vol_key, vol_values in prodct_value.iteritems():
                if final_external_accuracy_timeline.has_key(vol_key):
                    final_external_accuracy_timeline[vol_key] = final_external_accuracy_timeline[vol_key] + vol_values
                else:
                    final_external_accuracy_timeline[vol_key] = vol_values
        result_dict['external_accuracy_timeline'] = graph_data_alignment(final_external_accuracy_timeline,name_key='data')
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



def num_of_days(to_date,from_date):
    date_list=[]
    no_of_days = to_date - from_date
    no_of_days = int(re.findall('\d+', str(no_of_days))[0])
    for i in range(0, no_of_days + 1):
        date_list.append(str(from_date + timedelta(days=i)))
    return date_list


def fte_calculation(request,dwm_dict,prj_id,center_obj):
    query_set = {}
    query_set['project'] = prj_id
    query_set['center'] = center_obj
    work_packets = Targets.objects.filter(**query_set).values('sub_project','work_packet','sub_packet').distinct()
    import pdb;pdb.set_trace()
    pass

def top_five_emp(center,prj_id,dwm_dict):
    dict_to_render = []
    all_packets_list = RawTable.objects.filter(project=prj_id,center=center).values_list('work_packet').distinct()[1:]
    for one_pack in all_packets_list:
        max_value = RawTable.objects.filter(project=prj_id, center=center, work_packet=one_pack[0],
            date__range=[dwm_dict['days'][0], dwm_dict['days'][-1:][0]]).aggregate(Max('per_day'))['per_day__max']
        list_of_values = RawTable.objects.filter(project=prj_id, center=center, work_packet=one_pack[0],
            date__range=[dwm_dict['days'][0], dwm_dict['days'][-1:][0]], per_day=max_value).values('employee_id',
                            'date', 'per_day','work_packet')
        if len(list_of_values) > 0:
            list_of_values = list_of_values[0]
        else:
            continue
        for key, value in list_of_values.items():
            list_of_values[key] = str(value)
        dict_to_render.append(list_of_values)
    return dict_to_render


def from_to(request):
    from_date = datetime.datetime.strptime(request.GET['from'],'%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(request.GET['to'],'%Y-%m-%d').date()
    type = request.GET['type']

    #type='day'
    try:
        work_packet = request.GET.get('work_packet')
    except:
        work_packet = []
    try:
        sub_project = request.GET.get('sub_project')
    except:
        sub_project = ''
    try:
        sub_packet = request.GET.get('sub_packet')
    except:
        sub_packet = ''
    level_structure_key ={}
    if work_packet== 'all' :
        work_packet = 'undefined'
    if sub_project== 'all':
        sub_project ='undefined'
    if sub_packet == 'all':
        sub_packet = 'undefined'
    if (work_packet) and (work_packet !='undefined'): level_structure_key['work_packet']=work_packet
    if (sub_project) and (sub_project !='undefined'): level_structure_key['sub_project'] = sub_project
    if (sub_packet) and (sub_packet !='undefined'): level_structure_key['sub_packet'] = sub_packet

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
    """if type == 'day':
        dwm_dict['day']= date_list
    if type == 'month':
        dwm_dict['month'] = months_dict
    if type == 'week':
        dwm_dict['week'] = week_list"""

    employe_dates = {}
    if type == 'day':
        dwm_dict['day']= date_list
        employe_dates['days'] = date_list
    if type == 'month':
        dwm_dict['month'] = months_dict
        for month_name,month_values in months_dict.iteritems():
            if employe_dates.has_key('days'):
                employe_dates['days'] = employe_dates['days'].appeend(month_values)
            else:
                employe_dates['days']=month_values
    if type == 'week':
        dwm_dict['week'] = week_list
        for week in week_list:
            if week and  employe_dates.has_key('days'):
                employe_dates['days'] = employe_dates['days']+week
            else:
                employe_dates['days'] = week


    resul_data = {}
    center = Center.objects.filter(name=center_id).values_list('id', flat=True)
    prj_id = Project.objects.filter(name=project).values_list('id',flat=True)
    top_five_employee_details = top_five_emp(center,prj_id,employe_dates)
    final_result_dict = day_week_month(request,dwm_dict,prj_id,center,work_packet,level_structure_key)
    #fte_calc_data = fte_calculation(request,dwm_dict,prj_id,center)
    final_result_dict['top_five_employee_details'] = top_five_employee_details
    return HttpResponse(final_result_dict)
    #return HttpResponse(fte_calc_data)
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

