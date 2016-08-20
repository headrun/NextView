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
from django.db.models import Sum
import redis
from datetime import timedelta
from datetime import date
import re

def dashboard_insert(request):
    week_dates_list = []
    start_date = date.today() - timedelta(days=7)
    for i in range(0,7):
        week_dates_list.append(start_date + timedelta(days=i))
    week_list = set(week_dates_list)
    all_dates = []
    for date_val in week_list:
        part_date = str(date_val)
        all_dates.append(part_date)

    conn = redis.Redis(host="localhost", port=6379, db=0)
    result = {}
    volumes_dict = {}
    date_values = {}
    for date_va in all_dates:
        date_pattern = '*{0}*'.format(date_va)
        key_list = conn.keys(pattern=date_pattern)
        for cur_key in key_list:
            var = conn.hgetall(cur_key)
            for key,value in var.iteritems():
                if date_values.has_key(key):
                    date_values[key].append(int(value))
                else:
                    date_values[key]=[int(value)]
    volumes_dict['data'] = date_values
    volumes_dict['date'] = all_dates

    result['data'] = volumes_dict 
    print result
    return HttpResponse(result)

def error_insert(request):
    volumes_list = Error.objects.values_list('volume_type',flat=True).distinct()
    conn = redis.Redis(host="localhost", port=6379, db=0)
    result = {}
    volumes_dict = {}
    vol_error_values = {}
    vol_audit_data = {}
    for volume in volumes_list:
        key_pattern = '*{0}*error'.format(volume)
        key_list = conn.keys(pattern=key_pattern)
        for cur_key in key_list:
            var = conn.hgetall(cur_key)
            for key, value in var.iteritems():
                if key == 'total_errors':
                    if vol_error_values.has_key(volume):
                        vol_error_values[volume].append(int(value))
                    else:
                        vol_error_values[volume] = [int(value)]
                else:
                    if vol_audit_data.has_key(volume):
                        vol_audit_data[volume].append(int(value))
                    else:
                        vol_audit_data[volume] = [int(value)]

    error_volume_data = {}
    error_graph_data = []
    for key, value in vol_error_values.iteritems():
        error_graph = []
        error_volume_data[key] = sum(value)
        error_graph.append(key)
        error_graph.append(sum(value))
        error_graph_data.append(error_graph)
    error_audit_data={}
    for key, value in vol_audit_data.iteritems():
        error_audit_data[key] = sum(value)
    error_accuracy = {}
    for volume in volumes_list :
        percentage = (float(error_volume_data[volume])/error_audit_data[volume])*100
        percentage = float('%.2f' % round(percentage,2))
        error_accuracy[volume] = percentage
    total_graph_data = {}
    total_graph_data['error_count']= error_graph_data
    total_graph_data['accuracy_graph'] = error_accuracy

    print error_graph_data,error_accuracy


    return HttpResponse(total_graph_data)

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
        prj_id = Customer.objects.filter(name_id=request.user.id).values_list('project')[0][0]
        project = str(Project.objects.filter(id=prj_id)[0])
        return HttpResponse(project)

def redis_insert(prj_obj):
    prj_name = prj_obj.name
    data_dict = {}
    dates_list = RawTable.objects.values_list('date').distinct()
    all_dates = []
    for date in dates_list:
        part_date = str(date[0].date())
        all_dates.append(part_date)
        volumes_list = RawTable.objects.filter(date=date[0]).values_list('volume_type').distinct()
        for volume in volumes_list:
            value_dict = {}
            redis_key = '{0}_{1}_{2}'.format(prj_name,volume[0],part_date)
            total = RawTable.objects.filter(volume_type=volume[0],date=date[0]).values_list('per_day').aggregate(Sum('per_day'))
            value_dict[str(volume[0])] = str(total['per_day__sum'])
            data_dict[redis_key] = value_dict
    print data_dict,all_dates

    conn = redis.Redis(host="localhost", port=6379, db=0)
    current_keys = []
    for key,value in data_dict.iteritems():
        current_keys.append(key)
        conn.hmset(key,value)

def redis_insert_two(prj_obj):
    prj_name = prj_obj.name
    data_dict = {}
    #import pdb;pdb.set_trace()
    volumes_list = Error.objects.values_list('volume_type',flat=True).distinct()
    for volume in volumes_list:
        value_dict = {}
        dates_values = Error.objects.filter(volume_type=volume).values_list('date',flat=True)
        for date in dates_values:
            error_data = {}
            redis_key = '{0}_{1}_{2}_error'.format(prj_name, volume, date)
            audited_values = Error.objects.filter(date=date,volume_type=volume).values_list('audited_errors',flat=True)
            total_errors = Error.objects.filter(date=date,volume_type=volume).values_list('error_value',flat=True)
            error_data['audited_values'] = int(sum(audited_values))
            error_data['total_errors'] = int(sum(total_errors))
            data_dict[redis_key]=error_data

    print data_dict

    conn = redis.Redis(host="localhost", port=6379, db=0)
    current_keys = []
    for key, value in data_dict.iteritems():
        current_keys.append(key)
        conn.hmset(key, value)

def redis_insert_three(prj_obj):
    prj_name = prj_obj.name
    data_dict = {}
    #import pdb;pdb.set_trace()
    volumes_list = Externalerrors.objects.values_list('volume_type',flat=True).distinct()
    for volume in volumes_list:
        value_dict = {}
        dates_values = Externalerrors.objects.filter(volume_type=volume).values_list('date',flat=True).distinct()
        for date in dates_values:
            extr_error_data = {}
            redis_key = '{0}_{1}_{2}_externalerror'.format(prj_name, volume, date)
            avoidable_count = 0
            concept_count = 0
            total_error_count = 0
            extranal_data = Externalerrors.objects.filter(date=date,volume_type=volume).values('error_type','error_value','agent_reply')
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
            #import pdb;pdb.set_trace()
            print extr_error_data
            data_dict[redis_key]= extr_error_data

    print data_dict

    conn = redis.Redis(host="localhost", port=6379, db=0)
    current_keys = []
    for key, value in data_dict.iteritems():
        current_keys.append(key)
        conn.hmset(key, value)

def upload(request):
    """if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES['myfile'])
        if form.is_valid:
            newdoc = Document(document=request.FILES['myfile'])
            var = "general"
            #import pdb;pdb.set_trace()
            newdoc.save()"""
    teamleader_obj_name = TeamLead.objects.filter(name_id=request.user.id)[0]
    teamleader_obj = TeamLead.objects.filter(name_id=request.user.id).values_list('project_id')[0][0]
    prj_obj = Project.objects.filter(id=teamleader_obj)[0]
    center_obj = Center.objects.filter(id=Project.objects.filter(id=teamleader_obj).values_list('center_id',flat=True)[0])[0]
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
        #import pdb;pdb.set_trace()
        excel_sheet_names = open_book.sheet_names()
        file_sheet_name = Authoringtable.objects.values_list('sheet_name',flat=True).distinct()
        file_sheet_names = [x.encode('UTF8') for x in file_sheet_name]
        sheet_index_dict = {}
        for sh_name in file_sheet_names:
            if sh_name in excel_sheet_names:
                sheet_index_dict[sh_name] = open_book.sheet_names().index(sh_name)
        for key,value in sheet_index_dict.iteritems():
            customer_data = {}
            open_sheet = open_book.sheet_by_index(value)
            SOH_XL_HEADERS = open_sheet.row_values(0)
            main_headers = Authoringtable.objects.filter(sheet_name=sh_name).values_list('sheet_field',flat=True)
            sheet_main_headers = [x.encode('UTF8') for x in main_headers]
            table_schema = Authoringtable.objects.filter(sheet_name=sh_name).values_list('table_schema',flat=True)
            table_schema = [x.encode('UTF8') for x in table_schema]
            mapping_table={}
            for sh_filed,t_field in zip(sheet_main_headers,table_schema):
                mapping_table[sh_filed] = t_field
            SOH_XL_MAN_HEADERS = [x.title() for x in main_headers]
            sheet_headers = validate_sheet(open_sheet, request,SOH_XL_HEADERS,SOH_XL_MAN_HEADERS)

            for row_idx in range(1, open_sheet.nrows):
                error_type = {}
                for column, col_idx in sheet_headers:
                    cell_data = get_cell_data(open_sheet, row_idx, col_idx)
                    #if key == 'Error':
                    if column in ['avoidable','concept'] and key == 'Error':
                        column_name = mapping_table.get(column, '')
                        error_type[column_name] = ''.join(cell_data)
                    elif column !="date" and column in mapping_table.keys():
                        column_name = mapping_table.get(column,'')
                        customer_data[column_name] = ''.join(cell_data)
                    elif column == "date":
                        cell_data = xlrd.xldate_as_tuple(int(cell_data.split('.')[0]), 0)
                        cell_data = '%s-%s-%s' % (cell_data[0], cell_data[1], cell_data[2])
                        customer_data['date'] = ''.join(cell_data)

                volume_dict = {'DataDownload':'DD', 'CompanyCoordinates':'CC' , 'DetailFinancial':'DF','GroupCompanies':'GC','FES':'FES' ,
                               'Legal & CDR':'Legal' ,'DetailFinancial with FES':'DFES','Charges':'Charges',
                               'Compliance':'Compliance' ,'LLP':'LLP','Manual Download' : 'MD'}
                if customer_data['volume_type'] in volume_dict.keys():
                    customer_data['volume_type'] = volume_dict[customer_data['volume_type']]

                for sh_name in sheet_index_dict.keys():
                    if sh_name == 'Production':
                        try :
                            per_day_value = int(float(customer_data['cmplt_target']))
                        except ValueError:
                            per_day_value = 0
                        new_can = RawTable(project=prj_obj, employee=customer_data['emp_id'],
                                           volume_type=customer_data['volume_type'], per_hour=0,per_day=per_day_value,
                                           date=customer_data['date'], norm=int(float(customer_data['target'])),team_lead=teamleader_obj_name,center = center_obj)
                    if sh_name == 'Internal':
                        new_can = Error(employee_id=customer_data['employee_id'],
                                        volume_type=customer_data['volume_type'],
                                        date=customer_data['date'], audited_errors=int(float(customer_data['audited'])),
                                        error_value=int(float(customer_data['total_error'])), )

                    if sh_name == 'Error':
                        #import pdb;pdb.set_trace()
                        for er_key, er_value in error_type.iteritems():
                            if er_value:
                                new_can = Externalerrors(employee_id=customer_data['employee_id'],
                                                volume_type=customer_data['volume_type'],
                                                date=customer_data['date'], error_type=er_key,agent_reply=customer_data['agent_reply'], error_value=int(float(er_value)), )
                                try :
                                    new_can.save()
                                except :
                                    var = 'Duplicate Sheet'
                                    return HttpResponse(var)

                    if sh_name != 'Error':
                        try:
                            print customer_data
                            new_can.save()
                        except:
                            var = 'Duplicate Sheet'
                            return HttpResponse(var)
            if key == 'Production':
                insert = redis_insert(prj_obj)
            if key == 'Internal':
                insert = redis_insert_two(prj_obj)
            if key == 'Error':
                insert = redis_insert_three(prj_obj)
    #var ="hai"
    return HttpResponse(var)

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

def from_to(request):
    from_date = datetime.datetime.strptime(request.GET['from'],'%Y-%m-%d').date()
    to_date = datetime.datetime.strptime(request.GET['to'],'%Y-%m-%d').date()
    date_list = []
    no_of_days = to_date-from_date
    no_of_days = int(re.findall('\d+',str(no_of_days))[0])
    for i in range(0,no_of_days+1):
        date_list.append(str(from_date+timedelta(days=i)))
    conn = redis.Redis(host="localhost", port=6379, db=0)
    #below varaibles for productivity,wpf graphs
    result = {}
    volumes_dict = {}
    date_values = {}
    volume_list = RawTable.objects.values_list('volume_type', flat=True).distinct()
    extr_volumes_list = Externalerrors.objects.values_list('volume_type', flat=True).distinct()
    distinct_volumes = [x.encode('UTF8') for x in volume_list]
    #below variable for error graphs.
    vol_error_values = {}
    vol_audit_data = {}
    #below variable for external errors
    extrnl_error_values = {}
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
        # below code for error graphs

        key_pattern = '*{0}*_error'.format(date_va)
        audit_key_list = conn.keys(pattern=key_pattern)
        #import pdb;pdb.set_trace()
        for cur_key in audit_key_list:
            var = conn.hgetall(cur_key)
            for key, value in var.iteritems():
                error_vol_type = cur_key.split('_')[1]
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
        #import pdb;pdb.set_trace()
        extr_key_pattern = '*{0}*_externalerror'.format(date_va)
        extr_key_list = conn.keys(pattern=extr_key_pattern)
        # import pdb;pdb.set_trace()
        for cur_key in extr_key_list:
            var = conn.hgetall(cur_key)
            for key, value in var.iteritems():
                error_vol_type = cur_key.split('_')[1]
                if key == 'total_errors':
                    if extrnl_error_values.has_key(error_vol_type):
                        extrnl_error_values[error_vol_type].append(int(value))
                    else:
                        extrnl_error_values[error_vol_type] = [int(value)]
    #below code for productivity,wpf graph
    volumes_data = result['data']['data']
    volume_bar_data = {}
    volume_bar_data['volume_type']= volumes_data.keys()
    volume_keys_data ={}
    for key,value in volumes_data.iteritems():
        volume_keys_data[key]= sum(value)
    volume_list = RawTable.objects.values_list('volume_type',flat=True).distinct()
    distinct_volumes= [x.encode('UTF8') for x in volume_list]
    for vol in distinct_volumes :
        if vol not in volume_keys_data and "DetailFinancial" not in vol:
            volume_keys_data[vol]=0
    volume_list_data=[]
    volume_dict = {'DataDownload':'DD', 'CompanyCoordinates':'CC' , 'DetailFinancial':'DF','GroupCompanies':'GC','FES':'FES' ,
                               'Legal & CDR':'Legal' ,'DetailFinancial with FES ':'DF/FES','Charges':'Charges',
                               'Compliance':'Compliance' ,'LLP':'LLP','Manual Download' : 'MD'}


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
    #below code for error graphs
    error_dist_vol = Error.objects.values_list('volume_type', flat=True).distinct()
    error_volume_data = {}
    error_graph_data = []
    for key, value in vol_error_values.iteritems():
        error_graph = []
        if volume_dict.has_key(key):
            key = volume_dict[key]
            error_volume_data[key] = sum(value)
        else:
            error_volume_data[key] = sum(value)
        error_graph.append(key)
        error_graph.append(sum(value))
        error_graph_data.append(error_graph)
    volume_list = RawTable.objects.values_list('volume_type', flat=True).distinct()
    distinct_volumes = [x.encode('UTF8') for x in volume_list]
    for vol in distinct_volumes:
        if vol not in error_volume_data.keys() and "DetailFinancial" not in vol:
            if volume_dict.has_key(vol):
                error_volume_data[volume_dict[vol]] = 0
            else:
                error_volume_data[vol] = 0
    error_audit_data = {}
    for key, value in vol_audit_data.iteritems():
        error_audit_data[key] = sum(value)
    error_accuracy = {}
    for volume in error_dist_vol:
        if (volume in error_volume_data.keys()) and (volume in error_audit_data.keys()):
            percentage = (float(error_volume_data[volume]) / error_audit_data[volume]) * 100
            percentage = float('%.2f' % round(percentage, 2))
            error_accuracy[volume] = percentage
    #import pdb;pdb.set_trace()
    for vol in volume_list:
        if vol not in error_accuracy.keys() and "DetailFinancial" not in vol:
            if volume_dict.has_key(vol):
                error_accuracy[volume_dict[vol]]=0
            else:
                error_accuracy[vol]=0
    total_graph_data = {}
    #result['error_count'] = error_graph_data
    result['error_count'] = error_volume_data
    result['accuracy_graph'] = error_accuracy
    #below code for external graphs
    #import pdb;pdb.set_trace()
    extrnl_error_sum = {}
    for key,value in extrnl_error_values.iteritems():
        extrnl_error_sum[key] = sum(value)

    #beow code for external erro accuracy
    packet_sum_data = result['volumes_data']['volume_values']
    #import pdb;pdb.set_trace()
    extr_err_accuracy={}
    for er_key,er_value in extrnl_error_sum.iteritems():
        if packet_sum_data.has_key(er_key):
            percentage = (float(er_value) / packet_sum_data[er_key]) * 100
            percentage = 100  - float('%.2f' % round(percentage, 2))
            extr_err_accuracy[er_key] = percentage
    #print extr_err_accuracy
    for vol in volume_list:
        if vol not in extr_err_accuracy.keys() and "DetailFinancial" not in vol:
            if volume_dict.has_key(vol):
                extr_err_accuracy[volume_dict[vol]]=0
            else:
                extr_err_accuracy[vol]=0
        if vol not in extrnl_error_sum.keys() and "DetailFinancial" not in vol:
            if volume_dict.has_key(vol):
                extrnl_error_sum[volume_dict[vol]]=0
            else:
                extrnl_error_sum[vol]=0
    extr_err_acc_name = []
    extr_err_acc_perc = []
    for key,value in extr_err_accuracy.iteritems():
        extr_err_acc_name.append(key)
        extr_err_acc_perc.append(value)
    result['extr_err_accuracy'] = extr_err_accuracy
    result['extr_err_accuracy']['extr_err_name'] = extr_err_acc_name
    result['extr_err_accuracy']['extr_err_perc'] = extr_err_acc_perc
    result['extrn_error_count'] = extrnl_error_sum
    print result
    return HttpResponse(result)

def chart_data(request):
    #import pdb;pdb.set_trace()
    to_date = datetime.datetime.strptime(request.GET['date'], '%Y-%m-%d').date()
    work_packet = str(request.GET['packet'])
    packet_dict = {}
    emp_name = RawTable.objects.filter(date=to_date,volume_type=work_packet).values_list('employee',flat=True)
    packet_values = RawTable.objects.filter(date=to_date,volume_type=work_packet).values_list('per_day',flat=True)
    emp_names= [x.encode('UTF8') for x in emp_name]
    work_packet_values = [int(x) for x in packet_values]
    #import pdb;pdb.set_trace()

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

