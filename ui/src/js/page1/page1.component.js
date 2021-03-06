;(function (angular) {
  "use strict";

  angular.module("page1")
         .component("page1", {

           "templateUrl": "/js/page1/page1.html",
           "controller": ['$http','$scope',

           function ($http,$scope) {

             var self = this;
             var from_to = '/api/from_to/?'
             var error_api = '/api/error_board'
             var def_disp = '/api/default'
             var yesterdays_data = '/api/yesterdays_data'
             var someDate = new Date();
             var fi_dd = someDate.getDate();
             var fi_mm = someDate.getMonth() + 1;
             var fi_y = someDate.getFullYear();
             var firstDate = fi_y + '-' + fi_mm + '-' + fi_dd;
             var numberOfDaysToSub = 6;
             someDate.setDate(someDate.getDate() - numberOfDaysToSub);
             var la_dd = someDate.getDate();
             var la_mm = someDate.getMonth() + 1;
             var la_y = someDate.getFullYear();
             var lastDate = la_y + '-' + la_mm + '-' + la_dd;
             var project = 'api/project/';
             var drop_down_link = '/api/dropdown_data/';

             $('#select').daterangepicker({
                    "autoApply": true,
                    "locale": {
                        "format": 'YYYY-MM-DD'
                    },
              }, function(start, end, label) {
                self.start = start.format('YYYY-MM-DD');
                self.end = end.format('YYYY-MM-DD');
                self.click(start,end);
               });

             $http({method:"GET", url:project}).success(function(result){
                if (result.result.role === 'customer'){
                    $('#emp_widget').hide();    
                     }
                self.list_object = result.result.lay[0];
                /*self.list_object = result.result.lay[0];*/
                if((result.result.role === 'customer') || (result.result.role === 'team_lead') || (result.result.role === 'center_manager') || (result.result.role === 'nextwealth_manager'))
                {
                    var pro_cen_nam = result.result.list[1]
                    self.first = result.result.dates.from_date;
                    self.lastDate = self.first;
                    self.last = result.result.dates.to_date;
                    self.firstDate = self.last;
                    $('#select').val(self.first + ' to ' + self.last)

                    if ((result.result.role === 'customer') || (result.result.role === 'team_lead') || (result.result.role === 'nextwealth_manager') || (result.result.role === 'center_manager')){
                       self.layout_list = result.result.lay[1].layout;
                    }
                    else {
                        if (result.result.lay.length == 1){
                            self.layout_list = result.result.lay[0][pro_cen_nam]
                        }
                        else {
                            self.layout_list = result.result.lay[1][pro_cen_nam]
                        }
                    }
                    self.final_layout_values_list = {
                    'self.chartOptions':self.chartOptions,
                    'self.chartOptions4':self.chartOptions4,
                    'self.chartOptions6':self.chartOptions6,
                    'self.chartOptions9':self.chartOptions9,
                    'self.chartOptions9_2':self.chartOptions9_2,
                    'self.chartOptions10':self.chartOptions10,
                    'self.chartOptions15':self.chartOptions15,
                    'self.chartOptions15_2':self.chartOptions15_2,
                    'self.chartOptions16':self.chartOptions16,
                    'self.chartOptions16_2':self.chartOptions16_2,
                    'self.chartOptions17':self.chartOptions17,
                    'self.chartOptions18':self.chartOptions18,
                    'self.chartOptions5':self.chartOptions5,
                    'self.chartOptions5_2':self.chartOptions5_2,
                    'self.chartOptions19':self.chartOptions19,
                    'self.chartOptions20':self.chartOptions20,
                    'self.chartOptions21':self.chartOptions21,
                    };
                    /*self.list_object = {
                        "productivity_chart": {
                            'title': 'Production Trends',
                            'id': 1,
                            'col': 12,
                            'api': 'chartOptions',
                            'opt': self.chartOptions,
                            'widget': 1
                        },
                        "internal_error_accuracy": {
                            'title': 'Internal Accuracy',
                            'id': 2,
                            'col': 6,
                            'api': '',
                            'opt': self.chartOptions4,
                            'widget': 0
                        },
                        "external_error_accuracy": {
                            'title': 'External Accuracy',
                            'id': 3,
                            'col': 6,
                            'api': '',
                            'opt': self.chartOptions6,
                            'widget': 0
                        },
                        "internal_error_accuracy_pie":{
                            'title': 'Internal Accuracy Graph [PIE]',
                            'id': 4,
                            'col': 6,
                            'api': '',
                            'opt': self.chartOptions5,
                            'widget': 0
                        },
                        "external_error_accuracy_pie":{
                            'title': 'External Accuracy Graph [PIE]',
                            'id': 5,
                            'col': 6,
                            'api': '',
                            'opt': self.chartOptions5_2,
                            'widget': 0
                        },
                        "internal_accuracy_timeline": {
                            'title': 'Internal Accuracy Trends',
                            'id': 6,
                            'col': 12,
                            'api': 'chartOptions9',
                            'opt': self.chartOptions9,
                            'widget': 1
                        },
                        "external_accuracy_timeline": {
                            'title': 'External Accuracy Trends',
                            'id': 7,
                            'col': 12,
                            'api': 'chartOptions9_2',
                            'opt': self.chartOptions9_2,
                            'widget': 1
                        },
                        "productivity_bar_graph": {
                            'title': 'Production Chart',
                            'id': 8,
                            'col': 12,
                            'api': 'chartOptions10',
                            'opt': self.chartOptions10,
                            'widget': 1
                        },
                        "utilisation_wrt_work_packet": {
                            'title': 'Utilisation Trends',
                            'id': 9,
                            'col': 6,
                            'api': '',
                            'opt': self.chartOptions15,
                            'widget': 0
                        },
                        "utilisation_wrt_wp_date": {
                            'title': 'WorkPacket Utilisation Trends',
                            'id': 10,
                            'col': 6,
                            'api': '',
                            'opt': self.chartOptions15_2,
                            'widget': 0
                        },
                        "total_fte": {
                            'title': 'WorkPacket Wise FTE',
                            'id': 11,
                            'col': 12,
                            'api': '',
                            'opt': self.chartOptions16,
                            'widget': 0
                        },
                        "sum_total_fte": {
                            'title': 'Total FTE',
                            'id': 12,
                            'col': 6,
                            'api': '',
                            'opt': self.chartOptions16_2,
                            'widget': 0
                        },
                        "volume_bar_graph": {
                            'title': 'Volume Movement',
                            'id': 13,
                            'col': 12,
                            'api': 'chartOptions17',
                            'opt': self.chartOptions17,
                            'widget': 1
                        },
                        "volume_productivity_graph": {
                            'title': 'Production Vs Volume',
                            'id': 13,
                            'col': 6,
                            'api': 'chartOptions18',
                            'opt': self.chartOptions18,
                            'widget': 1
                        }
                    };*/
                    /*self.list_object_drilldown = {
                    "Production":[
                        "name",
                        "sub_packet",
                        "done"
                    ],
                    "Internal":[
                        "name",
                        "audited_count",
                        "total_errors"
                    ],
                    "External":[
                        "name",
                        "audited_count",
                        "total_errors"
                    ],
                    "Internal_Bar":[
                        "date",
                        "name",
                        "audited_count",
                        "total_errors"
                    ],
                    "External_Bar":[
                        "date",
                        "name",
                        "audited_count",
                        "total_errors"
                    ],
                    "Internal_Bar_Pie":[
                        "date",
                        "name",
                        "audited_count",
                        "total_errors"
                    ],
                    "External_Bar_Pie":[
                        "date",
                        "name",
                        "audited_count",
                        "total_errors"
                    ],
                    "Productivity_Bar":[
                        "name",
                        "sub_packet",
                        "done"
                    ]
                    };*/
                    var final_layout_list = [];
                    for (var single in self.layout_list){
                        for (var double in self.list_object){
                            if (self.layout_list[single] === double) {
                                final_layout_list.push(self.list_object[double])
                            }
                        }
                    }

                    var is_filled = 0;
                    var col_size = 0;
                    var first_row = [];
                    var second_row = [];
                    for (var one_lay in final_layout_list){
                        col_size = col_size + final_layout_list[one_lay].col;
                        if (col_size > 12){
                            is_filled = 1;
                            if (col_size >= 12){
                                col_size = 0;
                            }
                        }
                        if (is_filled){
                            second_row.push(final_layout_list[one_lay]);
                        }
                        else{
                            first_row.push(final_layout_list[one_lay]);
                        }
                        if ((col_size%12 == 0) | (col_size > 12)){
                            is_filled = 1;
                            if (col_size >= 12){
                                col_size = 0;
                            }
                        }
                    }
                    self.useful_layout.push(first_row,second_row);

                    self.location = pro_cen_nam.split('-')[0].replace(' ','') + ' - '
                    self.project = pro_cen_nam.split('-')[1].replace(' ','') + ' - '
                    var from_to_data = from_to + 'from=' + self.lastDate + '&to=' + self.firstDate + '&project=' + self.project
                            + '&center=' + self.location + '&type=' + self.day_type;
                    self.main_render(from_to_data)
                }
             })
             console.log(self.firstDate);
             console.log(self.lastDate);
             self.updateState();
             console.log('Hello from page1 yesh');
             $scope.options = self.tabData;
             self.main_render = function(from_to_data){
                 $http({method:"GET", url:from_to_data}).success(function(result){
                        var sub_project_level = result.result.sub_project_level;
                        var sub_packet_level = result.result.sub_packet_level;
                        var work_packet_level = result.result.work_packet_level;
                        self.global_packet_values = result.result.fin;
                        self.hideLoading();

                        self.top_employee_details =  result.result.top_five_employee_details;
                        self.top_five = result.result.only_top_five;
                        self.drop_list =  result.result.drop_value
                        self.sub_pro_sel = document.getElementById("0");
                        self.wor_pac_sel = document.getElementById("1");
                        self.sub_pac_sel = document.getElementById("2");
                        $("#0, #1, #2").unbind("change");

                            if (result.result.fin.sub_project) {
                                console.log('sub_projet_exist');
                            }
                            else {
                                $('#2').hide();
                                //$('#2').remove();
                                if (result.result.fin.work_packet) {
                                    console.log('work_packet_exist');
                                }
                                if (result.result.fin.sub_packet) {
                                    console.log('sub_packet_exist');
                                }
                                else {
                                    $('#1').hide();
                                    //$('#1').remove();
                                }
                            }
                        for (var sub_pro in self.drop_list) {
                            self.sub_pro_sel.options[self.sub_pro_sel.options.length] = new Option(sub_pro, sub_pro);
                        }
                        self.sub_pro_sel.onchange = function () {
                            self.wor_pac_sel.length = 1;
                            self.sub_pac_sel.length = 1;
                            if (this.selectedIndex < 1) {
                                self.wor_pac_sel.options[0].text = "All"
                                self.sub_pac_sel.options[0].text = "All"
                                return;
                            }
                            self.wor_pac_sel.options[0].text = "All"
                            for (var wor_pac in self.drop_list[this.value]) {
                                self.wor_pac_sel.options[self.wor_pac_sel.options.length] = new Option(wor_pac, wor_pac);
                            }
                            if (self.wor_pac_sel.options.length==2) {
                                //self.wor_pac_sel.selectedIndex=1;
                                self.wor_pac_sel.onchange();
                            }
                        }
                        self.sub_pro_sel.onchange();
                        self.wor_pac_sel.onchange = function () {
                            self.sub_pac_sel.length = 1;
                            if (this.selectedIndex < 1) {
                                self.sub_pac_sel.options[0].text = "All"
                                return;
                            }
                            self.sub_pac_sel.options[0].text = "All"

                            var sub_pac = self.drop_list[self.sub_pro_sel.value][this.value];
                            for (var i = 0; i < sub_pac.length; i++) {
                                self.sub_pac_sel.options[self.sub_pac_sel.options.length] = new Option(sub_pac[i], sub_pac[i]);
                            }
                            if (self.sub_pac_sel.options.length==2) {
                                self.sub_pac_sel.selectedIndex=1;
                                self.sub_pac_sel.onchange();
                            }
                            }
                            self.drop_work_pack = 'All';
                            self.drop_sub_proj = 'All';
                            self.drop_sub_pack = 'All';
                            if ((result.result.fin.sub_project) && (result.result.fin.work_packet)){
                                $('#0').on('change', function(){
                                            if (self.day_type === 'week'){
                                                $('.day').addClass('active');
                                                $('.day').siblings().removeClass('active');
                                            }
                                            if (self.day_type === 'month'){
                                                $('.day').addClass('active');
                                                $('.day').siblings().removeClass('active');
                                            }
                                            if (self.sel_type === 'day'){
                                                $('.day').addClass('active');
                                                $('.day').siblings().removeClass('active');
                                            }
                                            if (self.sel_type === 'week'){
                                                $('.week').addClass('active');
                                                $('.week').siblings().removeClass('active');
                                            }
                                            if (self.sel_type === 'month'){
                                                $('.month').addClass('active');
                                                $('.month').siblings().removeClass('active');
                                            }

                                    self.showLoading();
                                    self.drop_sub_proj = this.value;
                                    self.drop_work_pack = self.wor_pac_sel.value;
                                    self.drop_sub_pack = self.sub_pac_sel.value;
                        //$('.day').addClass('active');
                        //$('.day').siblings().removeClass('active');


                            var final_work =  '&sub_project=' + self.drop_sub_proj + '&sub_packet=' + self.drop_sub_pack +
                                '&work_packet=' + self.drop_work_pack
                            var dateEntered = document.getElementById('select').value
                            dateEntered = dateEntered.replace(' to ','to');
                            var from = dateEntered.split('to')[0].replace(' ','');
                            var to = dateEntered.split('to')[1].replace(' ','');
                            var placeholder = ''
                            /*var from_to_data = from_to + 'from=' + from + '&to=' + to + '&project=' + self.project
                                    + '&center=' + self.location + '&type=' + self.day_type  + final_work;*/
                            var from_to_data = from_to + 'from=' + from + '&to=' + to + '&project=' + self.project
                                    + '&center=' + self.location + '&type=' + 'day'  + final_work;
                            $http({method:"GET", url:from_to_data}).success(function(result){
                                self.hideLoading();
                                self.chart_render(result,self.project,self.location);
                            });
                                });
                                $('#1').on('change', function(){
                                            if (self.day_type === 'week'){
                                                $('.day').addClass('active');
                                                $('.day').siblings().removeClass('active');
                                            }
                                            if (self.day_type === 'month'){
                                                $('.day').addClass('active');
                                                $('.day').siblings().removeClass('active');
                                            }
                                            if (self.sel_type === 'day'){
                                                $('.day').addClass('active');
                                                $('.day').siblings().removeClass('active');
                                            }
                                            if (self.sel_type === 'week'){
                                                $('.week').addClass('active');
                                                $('.week').siblings().removeClass('active');
                                            }
                                            if (self.sel_type === 'month'){
                                                $('.month').addClass('active');
                                                $('.month').siblings().removeClass('active');
                                            }
                                    self.showLoading();
                                    self.drop_sub_proj = self.sub_pro_sel.value
                                    self.drop_work_pack = this.value;
                                    self.drop_sub_pack = self.sub_pac_sel.value;
                        //$('.day').addClass('active');
                        //$('.day').siblings().removeClass('active');

                            var final_work =  '&sub_project=' + self.drop_sub_proj + '&sub_packet=' + self.drop_sub_pack +
                                '&work_packet=' + self.drop_work_pack
                            var dateEntered = document.getElementById('select').value
                            dateEntered = dateEntered.replace(' to ','to');
                            var from = dateEntered.split('to')[0].replace(' ','');
                            var to = dateEntered.split('to')[1].replace(' ','');
                            var placeholder = ''
                            /*var from_to_data = from_to + 'from=' + from + '&to=' + to + '&project=' + self.project
                                    + '&center=' + self.location + '&type=' + self.day_type  + final_work;*/
                            var from_to_data = from_to + 'from=' + from + '&to=' + to + '&project=' + self.project
                                    + '&center=' + self.location + '&type=' + 'day'  + final_work;
                            $http({method:"GET", url:from_to_data}).success(function(result){
                                self.hideLoading();
                                self.chart_render(result,self.project,self.location);
                            });
                                });
                                    $('#2').on('change', function(){
                                            if (self.day_type === 'week'){
                                                $('.day').addClass('active');
                                                $('.day').siblings().removeClass('active');
                                            }
                                            if (self.day_type === 'month'){
                                                $('.day').addClass('active');
                                                $('.day').siblings().removeClass('active');
                                            }
                                            if (self.sel_type === 'day'){
                                                $('.day').addClass('active');
                                                $('.day').siblings().removeClass('active');
                                            }
                                            if (self.sel_type === 'week'){
                                                $('.week').addClass('active');
                                                $('.week').siblings().removeClass('active');
                                            }
                                            if (self.sel_type === 'month'){
                                                $('.month').addClass('active');
                                                $('.month').siblings().removeClass('active');
                                            }

                                        self.showLoading();
                                        self.drop_work_pack = self.wor_pac_sel.value;
                                        self.drop_sub_proj = self.sub_pro_sel.value;
                                        self.drop_sub_pack = this.value;
                        //$('.day').addClass('active');
                        //$('.day').siblings().removeClass('active');

                            var final_work =  '&sub_project=' + self.drop_sub_proj + '&sub_packet=' + self.drop_sub_pack + '&work_packet=' + self.drop_work_pack
                            var dateEntered = document.getElementById('select').value
                            dateEntered = dateEntered.replace(' to ','to');
                            var from = dateEntered.split('to')[0].replace(' ','');
                            var to = dateEntered.split('to')[1].replace(' ','');
                            var placeholder = ''
                            /*var from_to_data = from_to + 'from=' + from + '&to=' + to + '&project=' + self.project
                                    + '&center=' + self.location + '&type=' + self.day_type  + final_work;*/
                            var from_to_data = from_to + 'from=' + from + '&to=' + to + '&project=' + self.project
                                    + '&center=' + self.location + '&type=' + 'day'  + final_work;
                            $http({method:"GET", url:from_to_data}).success(function(result){
                                self.hideLoading();
                                self.chart_render(result,self.project,self.location);
                            });
                                    });

                            }
                            else {
                                if ((result.result.fin.work_packet) && (result.result.fin.sub_packet)){
                                    $('#0').on('change', function(){
                                        self.showLoading();
                                        self.drop_work_pack = this.value;
                                        self.drop_sub_proj = 'undefined';
                                        self.drop_sub_pack = self.sub_pac_sel.value;
                                            if (self.day_type === 'week'){
                                                $('.day').addClass('active');
                                                $('.day').siblings().removeClass('active');
                                            }
                                            if (self.day_type === 'month'){
                                                $('.day').addClass('active');
                                                $('.day').siblings().removeClass('active');
                                            }
                                            if (self.sel_type === 'day'){
                                                $('.day').addClass('active');
                                                $('.day').siblings().removeClass('active');
                                            }
                                            if (self.sel_type === 'week'){
                                                $('.week').addClass('active');
                                                $('.week').siblings().removeClass('active');
                                            }
                                            if (self.sel_type === 'month'){
                                                $('.month').addClass('active');
                                                $('.month').siblings().removeClass('active');
                                            }

                        //$('.day').addClass('active');
                        //$('.day').siblings().removeClass('active');

                            var final_work =  '&sub_project=' + self.drop_sub_proj + '&sub_packet=' + self.drop_sub_pack + '&work_packet=' + self.drop_work_pack
                            var dateEntered = document.getElementById('select').value
                            dateEntered = dateEntered.replace(' to ','to');
                            var from = dateEntered.split('to')[0].replace(' ','');
                            var to = dateEntered.split('to')[1].replace(' ','');
                            var placeholder = ''
                            /*var from_to_data = from_to + 'from=' + from + '&to=' + to + '&project=' + self.project
                                    + '&center=' + self.location + '&type=' + self.day_type  + final_work;*/
                            var from_to_data = from_to + 'from=' + from + '&to=' + to + '&project=' + self.project
                                    + '&center=' + self.location + '&type=' + 'day'  + final_work;
                            $http({method:"GET", url:from_to_data}).success(function(result){
                                self.hideLoading();
                                self.chart_render(result,self.project,self.location);
                            });
                                    });
                                }
                                else{
                                    if (result.result.fin.work_packet){
                                        self.pack_day_type = result.result.days_type;
                                        $('#0').on('change', function(){
                                            self.showLoading();
                                            self.drop_work_pack = this.value;
                                            self.drop_sub_proj = 'undefined';
                                            self.drop_sub_pack = 'undefined';
                                            if (self.day_type === 'week'){
                                                $('.day').addClass('active');
                                                $('.day').siblings().removeClass('active');
                                            }
                                            if (self.day_type === 'month'){
                                                $('.day').addClass('active');
                                                $('.day').siblings().removeClass('active');
                                            }
                                            if (self.sel_type === 'day'){
                                                $('.day').addClass('active');
                                                $('.day').siblings().removeClass('active');
                                            }
                                            if (self.sel_type === 'week'){
                                                $('.week').addClass('active');
                                                $('.week').siblings().removeClass('active');
                                            }
                                            if (self.sel_type === 'month'){
                                                $('.month').addClass('active');
                                                $('.month').siblings().removeClass('active');
                                            }
                                            var is_exist = self.drop_work_pack.indexOf('&');
                                            if (is_exist > 0){
                                                self.drop_work_pack = self.drop_work_pack.replace(' & ',' and ')
                                            }
                            var final_work =  '&sub_project=' + self.drop_sub_proj + '&sub_packet=' + self.drop_sub_pack + '&work_packet=' + self.drop_work_pack;
                            var dateEntered = document.getElementById('select').value
                            dateEntered = dateEntered.replace(' to ','to');
                            var from = dateEntered.split('to')[0].replace(' ','');
                            var to = dateEntered.split('to')[1].replace(' ','');
                            var placeholder = ''
                            /*var from_to_data = from_to + 'from=' + from + '&to=' + to + '&project=' + self.project
                                    + '&center=' + self.location + '&type=' + self.day_type  + final_work;*/
                            var from_to_data = from_to + 'from=' + from + '&to=' + to + '&project=' + self.project
                                    + '&center=' + self.location + '&type=' + 'day'  + final_work;
                            $http({method:"GET", url:from_to_data}).success(function(result){
                                self.chart_render(result,self.project,self.location);
                            });
                                    })
                                }
                                }
                                if (result.result.fin.sub_packet) {
                                    $('#1').on('change', function(){
                                            if (self.day_type === 'week'){
                                                $('.day').addClass('active');
                                                $('.day').siblings().removeClass('active');
                                            }
                                            if (self.day_type === 'month'){
                                                $('.day').addClass('active');
                                                $('.day').siblings().removeClass('active');
                                            }
                                            if (self.sel_type === 'day'){
                                                $('.day').addClass('active');
                                                $('.day').siblings().removeClass('active');
                                            }
                                            if (self.sel_type === 'week'){
                                                $('.week').addClass('active');
                                                $('.week').siblings().removeClass('active');
                                            }
                                            if (self.sel_type === 'month'){
                                                $('.month').addClass('active');
                                                $('.month').siblings().removeClass('active');
                                            }

                                        self.showLoading();
                                        self.drop_sub_pack = this.value;
                                        self.drop_sub_proj = 'undefined';
                                        self.drop_work_pack;
                        //$('.day').addClass('active');
                        //$('.day').siblings().removeClass('active');

            var final_work =  '&sub_project=' + self.drop_sub_proj + '&sub_packet=' + self.drop_sub_pack + '&work_packet=' + self.drop_work_pack
            var dateEntered = document.getElementById('select').value
            dateEntered = dateEntered.replace(' to ','to');
            var from = dateEntered.split('to')[0].replace(' ','');
            var to = dateEntered.split('to')[1].replace(' ','');
            var placeholder = ''
            /*var from_to_data = from_to + 'from=' + from + '&to=' + to + '&project=' + self.project
                    + '&center=' + self.location + '&type=' + self.day_type  + final_work;*/
            var from_to_data = from_to + 'from=' + from + '&to=' + to + '&project=' + self.project
                    + '&center=' + self.location + '&type=' + 'day'  + final_work;
            $http({method:"GET", url:from_to_data}).success(function(result){
                            self.chart_render(result,self.project,self.location);
            });

                                    });
                                }
                                else {
                                    self.drop_sub_pack = 'undefined';
                                    console.log('sub_packet_not_exist');
                                }
                            }
                        self.packet_count = result.result.productivity_data.length;
                            self.chart_render(result,self.project,self.location);
                         })
                            }
                        self.removeOptions = function (selectbox){
                            var i;
                            for(i = selectbox.options.length - 1 ; i >= 0 ; i--)
                                {
                                    selectbox.remove(i);
                                }
                            }
             var unWatch;

             this.$onInit = function () {
                unWatch = $scope.$watch(function(scope) {
                    return scope.options.state;
                },
                function(newVal){
                    if (newVal.state) {
                        self.showLoading();
                        self.location = newVal.state.split(' - ')[0] + ' - ';
                        self.project = newVal.state.split(' - ')[1] + ' - ';
                        $('#0').show();
                        $('#1').show();
                        $('#2').show();
                        /*var sub_pa_se = 0;
                        var wor_pa_se = 1;
                        var sub_pr_se = 0;
                        if ((sub_pa_se === 0) && (sub_pr_se === 0)){
                            $('#1').prop('disabled', 'disabled');
                            $('#2').prop('disabled', 'disabled');
                        }
                        $('#0').remove();
                        $('#1').remove();
                        $('#2').remove();*/
                        //$('')
                        self.sub_pro_sel = document.getElementById("0");
                        self.removeOptions(self.sub_pro_sel);
                        self.wor_pac_sel = document.getElementById("1");
                        if (self.wor_pac_sel != null){
                            self.removeOptions(self.wor_pac_sel);
                        }
                        self.sub_pac_sel = document.getElementById("2");
                        if (self.sub_pac_sel != null){
                            self.removeOptions(self.sub_pac_sel);
                        }
                        var url_to_call = 'api/project/?name=' + self.project;
                        $http({method:"GET", url:url_to_call}).success(function(result){
                            var pro_cen_nam = result.result.list[1]
                            self.first = result.result.dates.from_date;
                            self.lastDate = self.first;
                            self.last = result.result.dates.to_date;
                            self.firstDate = self.last;
                        $('#select').val(self.first + ' to ' + self.last)
                        $("#0").append(new Option("All"));
                        $("#1").append(new Option("All"));
                        $("#2").append(new Option("All"));
                        $('.day').addClass('active');
                        $('.day').siblings().removeClass('active');
                        if (self.project == "Wallmart - "){
                            var from_to_data = from_to + 'from=' + self.lastDate + '&to=' + self.firstDate + '&project=' + 'DellBilling - ' +
                                '&center=' + 'Salem - ' + '&type=' + self.day_type;
                        }
                        else
                        {
                         var from_to_data = from_to + 'from=' + self.lastDate + '&to=' + self.firstDate + '&project=' + self.project +
                          '&center=' + self.location + '&type=' + 'day';
                        }
                        self.tabData.state = JSON.parse("{}");
                        self.main_render(from_to_data)
                        });
                    }
                });
             };
             this.$onDestroy = function () {
               return unWatch && unWatch();
             }
             var from_to_data = from_to + 'from=' + self.lastDate + '&to=' + self.firstDate + '&project=' + self.project
                         + '&center=' + self.location;

                self.last = self.firstDate;
                self.first = self.lastDate;

            self.dateType = function(key,all_data,name,button_clicked){
                self.showLoading();
                self.day_type = key;
                var obj = {"self.chartOptions":self.chartOptions,"self.chartOptions9":self.chartOptions9,"self.chartOptions9_2":self.chartOptions9_2,"self.chartOptions10":self.chartOptions10,"self.chartOptions15":self.chartOptions15,"self.chartOptions16":self.chartOptions16,"self.chartOptions16_2":self.chartOptions16_2,"self.chartOptions17":self.chartOptions17,"self.chartOptions18":self.chartOptions18,"self.chartOptions19":self.chartOptions19,"self.chartOptions20":self.chartOptions20,'self.chartOptions21':self.chartOptions21}
                self.render_data = obj[all_data];
                self.high_data = [];
                self.button_clicked = button_clicked;
                self.packet_clicked = self.drop_work_pack;
                var is_exist = self.packet_clicked.indexOf('&');
                if (is_exist > 0){
                    self.packet_clicked = self.packet_clicked.replace(' & ',' and ')
                }
                var final_work =  '&sub_project=' + self.drop_sub_proj + '&sub_packet=' + self.drop_sub_pack + '&work_packet=' + self.packet_clicked + '&is_clicked=' + self.button_clicked;
                var dateEntered = document.getElementById('select').value;
                dateEntered = dateEntered.replace(' to ','to');
                var from = dateEntered.split('to')[0].replace(' ','');
                var to = dateEntered.split('to')[1].replace(' ','');
                var from_to_data = from_to + 'from=' + from + '&to=' + to + '&project=' + self.project
                         + '&center=' + self.location + '&type=' + self.day_type + final_work;
                console.log(from_to_data);
                $http({method:"GET", url:from_to_data}).success(function(result){
                            self.hideLoading();
                            self.high_data_gener = [];
                            var final_data_gener = result.result;
                            self.high_data_gener.push(final_data_gener);
                            if (name === 'chartOptions'){
                            angular.extend(self.render_data, {
               xAxis: {
                 categories: self.high_data_gener[0].data.date,
                 title: {
                  text: '',
                 }
               },
               plotOptions: {
                series : {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    point: {
                        events:{
                        select: function(e) {
                        var chart_name = 'productivity_chart';
                        var is_drill = self.list_object[chart_name].is_drilldown;
                        if (is_drill){
                        var addition = '&project=' +self.project + '&center=' +self.location;
                        console.log(e.target.series.name);
                        var productivity_graph ='/api/chart_data/?'
                        self.packet_clicked = e.target.series.name;
                        var is_exist = self.packet_clicked.indexOf('&');
                        if (is_exist > 0){
                        self.packet_clicked = self.packet_clicked.replace(' & ',' and ')
                        }
                        $http.get( productivity_graph+ 'packet=' + self.packet_clicked + '&date=' + e.target.category +
                        '&type=' + 'Production Trends' + addition).success(
                        function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    var proj = data.result.project;
                                    //var pro_drill = drilldown_config[proj];
                                    var pro_drill = data.result.table_headers;
                                    var chart_type = data.result.type;
                                    //self.fields_list_drilldown = pro_drill[chart_type];
                                    self.fields_list_drilldown = pro_drill;
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                                }

                        }
                    }
                },
                bar: {
                 dataLabels: {
                 enabled: true
                 }
                }
               }
               },
               series: self.high_data_gener[0].productivity_data
             });
             }
             if (name === 'chartOptions10'){
                            angular.extend(self.render_data, {
               xAxis: {
                 categories: self.high_data_gener[0].data.date,
                 title: {
                  text: '',
                 }
               },
               plotOptions: {
                series : {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    point: {
                        events:{
                        select: function(e) {
                        var chart_name = 'productivity_bar_graph';
                        var is_drill = self.list_object[chart_name].is_drilldown;
                        if (is_drill){
                        var addition = '&project=' +self.project + '&center=' +self.location;
                        console.log(e.target.series.name);
                        var productivity_graph ='/api/chart_data/?'
                        self.packet_clicked = e.target.series.name;
                        var is_exist = self.packet_clicked.indexOf('&');
                        if (is_exist > 0){
                        self.packet_clicked = self.packet_clicked.replace(' & ',' and ')
                        }
                        $http.get( productivity_graph+ 'packet=' + self.packet_clicked + '&date=' + e.target.category +
                        '&type=' + 'Production Chart' + addition).success(
                        function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    var proj = data.result.project;
                                    var pro_drill = data.result.table_headers;
                                    //var pro_drill = drilldown_config[proj];
                                    var chart_type = data.result.type;
                                    self.fields_list_drilldown = pro_drill;
                                    //self.fields_list_drilldown = pro_drill[chart_type];
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                                }
               }
                    }
                },
                bar: {
                 dataLabels: {
                 enabled: true
                 }
                }
               }
               },
               series: self.high_data_gener[0].productivity_data
                     });
             }

           if (name === 'chartOptions16'){
                            angular.extend(self.render_data, {
               xAxis: {
                 categories: self.high_data_gener[0].data.date,
                 title: {
                  text: '',
                 }
               },
               plotOptions: {
                series : {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    point: {
                        events:{
                        select: function(e) {
                        var chart_name = 'total_fte';
                        var is_drill = self.list_object[chart_name].is_drilldown;
                        if (is_drill){
                        var addition = '&project=' +self.project + '&center=' +self.location;
                        console.log(e.target.series.name);
                        var productivity_graph ='/api/chart_data/?'
                        self.packet_clicked = e.target.series.name;
                        var is_exist = self.packet_clicked.indexOf('&');
                        if (is_exist > 0){
                        self.packet_clicked = self.packet_clicked.replace(' & ',' and ')
                        }
                        $http.get( productivity_graph+ 'packet=' + self.packet_clicked + '&date=' + e.target.category +
                        '&type=' + 'FTE Utilized _Workpacket Wise' + addition).success(
                        function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    var proj = data.result.project;
                                    var pro_drill = drilldown_config[proj];
                                    var chart_type = data.result.type;
                                    self.fields_list_drilldown = pro_drill[chart_type];
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                                }
               }
                    }
                },
                bar: {
                 dataLabels: {
                 enabled: true
                 }
                }
               }
               },
               series: self.high_data_gener[0].fte_calc_data.work_packet_fte
                     });
             } 

            if (name === 'chartOptions16_2'){
                            angular.extend(self.render_data, {
               xAxis: {
                 categories: self.high_data_gener[0].data.date,
                 title: {
                  text: '',
                 }
               },
               plotOptions: {
                series : {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    point: {
                        events:{
                        select: function(e) {
                        var chart_name = 'sum_total_fte';
                        var is_drill = self.list_object[chart_name].is_drilldown;
                        if (is_drill){
                        var addition = '&project=' +self.project + '&center=' +self.location;
                        console.log(e.target.series.name);
                        var productivity_graph ='/api/chart_data/?'
                        self.packet_clicked = e.target.series.name;
                        var is_exist = self.packet_clicked.indexOf('&');
                        if (is_exist > 0){
                        self.packet_clicked = self.packet_clicked.replace(' & ',' and ')
                        }
                        $http.get( productivity_graph+ 'packet=' + self.packet_clicked + '&date=' + e.target.category +
                        '&type=' + 'Total FTE Utilized' + addition).success(
                        function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    var proj = data.result.project;
                                    var pro_drill = drilldown_config[proj];
                                    var chart_type = data.result.type;
                                    self.fields_list_drilldown = pro_drill[chart_type];
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                                }
               }
                    }
                },
                bar: {
                 dataLabels: {
                 enabled: true
                 }
                }
               }
               },
               series: self.high_data_gener[0].fte_calc_data.total_fte
                     });
             }

            if (name === 'chartOptions20'){
                            angular.extend(self.render_data, {
               xAxis: {
                 categories: self.high_data_gener[0].data.date,
                 title: {
                  text: '',
                 }
               },
               plotOptions: {
                series : {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    point: {
                        events:{
                        select: function(e) {
                        var chart_name = 'internal_pareto_ analysis';
                        var is_drill = self.list_object[chart_name].is_drilldown;
                        if (is_drill){
                        var addition = '&project=' +self.project + '&center=' +self.location;
                        console.log(e.target.series.name);
                        var productivity_graph ='/api/chart_data/?'
                        self.packet_clicked = e.target.series.name;
                        var is_exist = self.packet_clicked.indexOf('&');
                        if (is_exist > 0){
                        self.packet_clicked = self.packet_clicked.replace(' & ',' and ')
                        }
                        $http.get( productivity_graph+ 'packet=' + self.packet_clicked + '&date=' + e.target.category +
                        '&type=' + 'Internal Pareto Analysis' + addition).success(
                        function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    var proj = data.result.project;
                                    var pro_drill = drilldown_config[proj];
                                    var chart_type = data.result.type;
                                    self.fields_list_drilldown = pro_drill[chart_type];
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                                }
               }
                    }
                },
                bar: {
                 dataLabels: {
                 enabled: true
                 }
                }
               }
               },
               series: self.high_data_gener[0].internal_pareto_graph_data
                     });
             }

           if (name === 'chartOptions21'){
                            angular.extend(self.render_data, {
               xAxis: {
                 categories: self.high_data_gener[0].data.date,
                 title: {
                  text: '',
                 }
               },
               plotOptions: {
                series : {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    point: {
                        events:{
                        select: function(e) {
                        var chart_name = 'external_pareto_ analysis';
                        var is_drill = self.list_object[chart_name].is_drilldown;
                        if (is_drill){
                        var addition = '&project=' +self.project + '&center=' +self.location;
                        console.log(e.target.series.name);
                        var productivity_graph ='/api/chart_data/?'
                        self.packet_clicked = e.target.series.name;
                        var is_exist = self.packet_clicked.indexOf('&');
                        if (is_exist > 0){
                        self.packet_clicked = self.packet_clicked.replace(' & ',' and ')
                        }
                        $http.get( productivity_graph+ 'packet=' + self.packet_clicked + '&date=' + e.target.category +
                        '&type=' + 'External Pareto Analysis' + addition).success(
                        function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    var proj = data.result.project;
                                    var pro_drill = drilldown_config[proj];
                                    var chart_type = data.result.type;
                                    self.fields_list_drilldown = pro_drill[chart_type];
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                                }
               }
                    }
                },
                bar: {
                 dataLabels: {
                 enabled: true
                 }
                }
               }
               },
               series: self.high_data_gener[0].external_pareto_graph_data
                     });
             } 


            if (name === 'chartOptions15'){
                angular.extend(self.render_data,{
                            xAxis: {
                                categories: self.high_data_gener[0].data.date,
                                title: {
                                    text: '',
                                }
                            },
                            plotOptions: {
                series : {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    point: {   
                        events:{
                            select: function(e) {
                            var chart_name = 'utilisation_wrt_work_packet';
                            var is_drill = self.list_object[chart_name].is_drilldown;
                            if (is_drill){
                            var addition = '&project=' + self.project + '&center=' + self.location;
                            console.log(e.target.series.name);
                            var productivity_graph ='/api/chart_data/?'
                                                 self.packet_clicked = e.target.series.name;
                                                 var is_exist = self.packet_clicked.indexOf('&');
                                                 if (is_exist > 0){
                                                    self.packet_clicked = self.packet_clicked.replace(' & ',' and ')
                                                 }
                            $http.get( productivity_graph+ 'packet=' + self.packet_clicked + '&date=' + e.target.category +
                             '&type=' + 'Utilisation Trends' + addition).success(
                            function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    var proj = data.result.project;
                                    var pro_drill = drilldown_config[proj];
                                    var chart_type = data.result.type;
                                    self.fields_list_drilldown = pro_drill[chart_type];
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                   }).error(function(error){ console.log("error")});
                                }
               }
                    }
                },   
                bar: {
                 dataLabels: {
                 enabled: true 
                 }
                }
               }
               },   
               series: self.high_data_gener[0].original_utilization_graph
                     });  
             }
 



             if (name === 'chartOptions9'){
                angular.extend(self.render_data,{
                            xAxis: {
                                categories: self.high_data_gener[0].data.date,
                                title: {
                                    text: '',
                                }
                            },
                            plotOptions: {
                series : {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    point: {
                        events:{
                            select: function(e) {
                            var chart_name = 'internal_accuracy_timeline';
                            var is_drill = self.list_object[chart_name].is_drilldown;
                            if (is_drill){
                            var addition = '&project=' + self.project + '&center=' + self.location;
                            console.log(e.target.series.name);
                            var productivity_graph ='/api/chart_data/?'
                                                 self.packet_clicked = e.target.series.name;
                                                 var is_exist = self.packet_clicked.indexOf('&');
                                                 if (is_exist > 0){
                                                    self.packet_clicked = self.packet_clicked.replace(' & ',' and ')
                                                 }
                            $http.get( productivity_graph+ 'packet=' + self.packet_clicked + '&date=' + e.target.category +
                             '&type=' + 'Internal Accuracy Trends' + addition).success(
                            function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    var proj = data.result.project;
                                    var pro_drill = data.result.table_headers;
                                    //var pro_drill = drilldown_config[proj];
                                    var chart_type = data.result.type;
                                    self.fields_list_drilldown = pro_drill;
                                    //self.fields_list_drilldown = pro_drill[chart_type];
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                                }
                        }
                    }
                    }
                },
                bar: {
                 dataLabels: {
                 enabled: true
                 }
                }
               },
                            series: self.high_data_gener[0].internal_time_line
                            });
             }
        
            if (name === 'chartOptions19'){
                angular.extend(self.render_data,{
                            xAxis: {
                                categories: self.high_data_gener[0].data.date,
                                title: {
                                    text: '',
                                }
                            },   
                            plotOptions: {
                series : {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    point: {
                        events:{
                            select: function(e) {
                            var chart_name = 'productivity_trends';
                            var is_drill = self.list_object[chart_name].is_drilldown;
                            if (is_drill){
                            var addition = '&project=' + self.project + '&center=' + self.location;
                            console.log(e.target.series.name);
                            var productivity_graph ='/api/chart_data/?'
                                                 self.packet_clicked = e.target.series.name;
                                                 var is_exist = self.packet_clicked.indexOf('&');
                                                 if (is_exist > 0){
                                                    self.packet_clicked = self.packet_clicked.replace(' & ',' and ')
                                                 }
                            $http.get( productivity_graph+ 'packet=' + self.packet_clicked + '&date=' + e.target.category +
                             '&type=' + 'Productivity trends' + addition).success(
                            function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    var proj = data.result.project;
                                    var pro_drill = drilldown_config[proj];
                                    var chart_type = data.result.type;
                                    self.fields_list_drilldown = pro_drill[chart_type];
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                                }
                        }
                    }
                    }
                },   
                bar: {
                 dataLabels: {
                 enabled: true 
                 }
                }
               },   
                            series: self.high_data_gener[0].original_productivity_graph
                            });  
             }



            if (name === 'chartOptions9_2'){
                angular.extend(self.render_data,{
                            xAxis: {
                                categories: self.high_data_gener[0].data.date,
                                title: {
                                    text: '',
                                }
                            },
                            plotOptions: {
                series : {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    point: {
                        events:{
                            select: function(e) {
                            var chart_name = 'external_accuracy_timeline';
                            var is_drill = self.list_object[chart_name].is_drilldown;
                            if (is_drill){
                            var addition = '&project=' + self.project + '&center=' + self.location;
                            console.log(e.target.series.name);
                            var productivity_graph ='/api/chart_data/?'
                                                 self.packet_clicked = e.target.series.name;
                                                 var is_exist = self.packet_clicked.indexOf('&');
                                                 if (is_exist > 0){
                                                    self.packet_clicked = self.packet_clicked.replace(' & ',' and ')
                                                 }
                            $http.get( productivity_graph+ 'packet=' + self.packet_clicked + '&date=' + e.target.category +
                             '&type=' + 'External Accuracy Trends' + addition).success(
                            function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    var proj = data.result.project;
                                    var pro_drill = data.result.table_headers;
                                    //var pro_drill = drilldown_config[proj];
                                    var chart_type = data.result.type;
                                    self.fields_list_drilldown = pro_drill;
                                    //self.fields_list_drilldown = pro_drill[chart_type];
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                                }
                        }
                    }
                    }
                },
                bar: {
                 dataLabels: {
                 enabled: true
                 }
                }
               },
                            series: self.high_data_gener[0].external_time_line
                            }); 
            }
            if (name === 'chartOptions17'){
                            angular.extend(self.render_data, {
                            xAxis: {
                                categories: self.high_data_gener[0].data.date,
                            },   
                            series: self.high_data_gener[0].volume_graphs.bar_data
                            });  
                            angular.extend(self.render_data.plotOptions.series.point.events,{
                            select: function(e) {
                            var addition = '&project=' + pro + '&center=' + loc; 
                            console.log(e.target.name);
                            var productivity_bar_graph ='/api/chart_data/?';
                            var dates_list = self.get_date();
                            $http.get( productivity_bar_graph + 'packet=' + e.target.series.name + '&date=' + e.target.category
                             + '&type=' + 'Production Chart'+addition).success(
                            function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    self.fields_list_drilldown = self.list_object_drilldown[data.result.type];
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});

                            }
                            });

            }
            if (name === 'chartOptions18'){
                                            angular.extend(self.render_data, {
                                xAxis: {
                                    categories: self.high_data_gener[0].data.date,
                                    title: {
                                        text: '',
                                    }
                                },
                                plotOptions: {
                                    series : {
                                        allowPointSelect: true,
                                        cursor: 'pointer',
                                        point: {
                                            events:{
                                             select: function(e) {

                                             var addition = '&project=' +pro + '&center=' +loc;
                                             console.log(e.target.series.name);
                                             var productivity_graph ='/api/chart_data/?'
                                             var packet_clicked = e.target.series.name;
                                             var is_exist = packet_clicked.indexOf('&');
                                             if (is_exist > 0){
                                                packet_clicked = packet_clicked.replace(' & ',' and ')
                                             }
                            $http.get( productivity_graph+ 'packet=' + packet_clicked + '&date=' + e.target.category +
                            '&type=' + 'Production Trends' + addition).success(
                            function(data, status)
                                {

                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    self.fields_list_drilldown = self.list_object_drilldown[data.result.type];
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                        }
                    }
                    }
                },
                bar: {
                 dataLabels: {
                 enabled: true
                 }
                }
               },
               series: self.high_data_gener[0].volume_graphs.line_data
             });
 
            }
                         });
            }
            self.chart_render = function(result,pro,loc){
                            self.hideLoading();
                            self.high_data_gener = [];
                            var final_data_gener = result.result;
                            self.high_data_gener.push(final_data_gener);
                            self.top_employee_details =  result.result.top_five_employee_details;
                            self.top_five = result.result.only_top_five;
                            angular.extend(self.chartOptions, {
                                xAxis: {
                                    categories: self.high_data_gener[0].data.date,
                                    title: {
                                        text: '',
                                    }
                                },
                                plotOptions: {
                                    series : {
                                        allowPointSelect: true,
                                        cursor: 'pointer',
                                        point: {
                                            events:{
                                             select: function(e) {
                                             var chart_name = 'productivity_chart';
                                             var is_drill = self.list_object[chart_name].is_drilldown;
                                             if (is_drill){
                                             var addition = '&project=' +pro + '&center=' +loc;
                                             console.log(e.target.series.name);
                                             var productivity_graph ='/api/chart_data/?'
                                             var packet_clicked = e.target.series.name;
                                             var is_exist = packet_clicked.indexOf('&');
                                             if (is_exist > 0){
                                                packet_clicked = packet_clicked.replace(' & ',' and ')
                                             }
                            $http.get( productivity_graph+ 'packet=' + packet_clicked + '&date=' + e.target.category +
                            '&type=' + 'Production Trends' + addition).success(
                            function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    var proj = data.result.project;
                                    var pro_drill = data.result.table_headers;
                                    var chart_type = data.result.type;
                                    self.fields_list_drilldown = pro_drill;
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                                }
                        }
                    }
                    }
                },
                bar: {
                 dataLabels: {
                 enabled: true
                 }
                }
               },
               series: self.high_data_gener[0].productivity_data
             });

                            angular.extend(self.chartOptions9_2.yAxis,{
                                min:result.result.min_external_time_line,
                                max:result.result.max_external_time_line
                            });
                            angular.extend(self.chartOptions9_2, {
                            xAxis: {
                                categories: self.high_data_gener[0].data.date,
                                title: {
                                    text: '',
                                }
                            },
plotOptions: {
                series : {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    point: {
                        events:{
                            select: function(e) {
                            var chart_name = 'external_accuracy_timeline';
                            var is_drill = self.list_object[chart_name].is_drilldown;
                            if (is_drill){
                            var addition = '&project=' + pro + '&center=' + loc;
                            console.log(e.target.series.name);
                            var productivity_graph ='/api/chart_data/?'
                                                 var packet_clicked = e.target.series.name;
                                                 var is_exist = packet_clicked.indexOf('&');
                                                 if (is_exist > 0){
                                                    packet_clicked = packet_clicked.replace(' & ',' and ')
                                                 }

                            $http.get( productivity_graph+ 'packet=' + packet_clicked + '&date=' + e.target.category +
                             '&type=' + 'External Accuracy Trends' + addition).success(
                            function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    var proj = data.result.project;
                                    var pro_drill = data.result.table_headers;
                                    var chart_type = data.result.type;
                                    self.fields_list_drilldown = pro_drill[chart_type];
                                    self.fields_list_drilldown = pro_drill;
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                                }
                        }
                    }
                    }
                },
                bar: {
                 dataLabels: {
                 enabled: true
                 }
                }
               },

                            series: self.high_data_gener[0].external_time_line
                            });
                            angular.extend(self.chartOptions9.yAxis,{
                                min:result.result.min_internal_time_line,
                                max:result.result.max_internal_time_line
                            });
                            angular.extend(self.chartOptions9, {
                            xAxis: {
                                categories: self.high_data_gener[0].data.date,
                                title: {
                                    text: '',
                                }
                            },
plotOptions: {
                series : {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    point: {
                        events:{
                            select: function(e) {
                            var chart_name = 'internal_accuracy_timeline';
                            var is_drill = self.list_object[chart_name].is_drilldown;
                            if (is_drill){
                            var addition = '&project=' + pro + '&center=' + loc;
                            console.log(e.target.series.name);
                            var productivity_graph ='/api/chart_data/?'
                                                 var packet_clicked = e.target.series.name;
                                                 var is_exist = packet_clicked.indexOf('&');
                                                 if (is_exist > 0){
                                                    packet_clicked = packet_clicked.replace(' & ',' and ')
                                                 }

                            $http.get( productivity_graph+ 'packet=' + packet_clicked + '&date=' + e.target.category +
                             '&type=' + 'Internal Accuracy Trends' + addition).success(
                            function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    var proj = data.result.project;
                                    var pro_drill = data.result.table_headers;
                                    var chart_type = data.result.type;
                                    self.fields_list_drilldown = pro_drill;
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                                }
                        }
                    }
                    }
                },
                bar: {
                 dataLabels: {
                 enabled: true
                 }
                }
               },
                            series: self.high_data_gener[0].internal_time_line
                            });
                            angular.extend(self.chartOptions19, {
                            xAxis: {
                                categories: self.high_data_gener[0].data.date,
                                title: {
                                    text: '',
                                }
                            },
plotOptions: {
                series : {
                    allowPointSelect: true,
                    cursor: 'pointer'
                },
                bar: {
                 dataLabels: {
                 enabled: true
                 }
                }
               },
                            series: self.high_data_gener[0].original_productivity_graph
                            });
                            angular.extend(self.chartOptions20, {
                            xAxis: {
                                categories: self.high_data_gener[0].data.date,
                                title: {
                                    text: '',
                                }
                            },
plotOptions: {
                series : {
                    allowPointSelect: true,
                    cursor: 'pointer'
                },
                bar: {
                 dataLabels: {
                 enabled: true
                 }
                }
               },
                            series: self.high_data_gener[0].internal_pareto_graph_data
                            });

                            angular.extend(self.chartOptions21, {
                            xAxis: {
                                categories: self.high_data_gener[0].data.date,
                                title: {
                                    text: '',
                                }
                            },
plotOptions: {
                series : {
                    allowPointSelect: true,
                    cursor: 'pointer'
                },
                bar: {
                 dataLabels: {
                 enabled: true
                 }
                }
               },
                            series: self.high_data_gener[0].external_pareto_graph_data
                            });

                            angular.extend(self.chartOptions10, {
                            xAxis: {
                                categories: self.high_data_gener[0].data.date
                            },
                            series: self.high_data_gener[0].productivity_data
                            });
                            angular.extend(self.chartOptions10.plotOptions.series.point.events,{
                            select: function(e) {
                            var chart_name = 'productivity_bar_graph';
                            var is_drill = self.list_object[chart_name].is_drilldown;
                            if (is_drill){
                            var addition = '&project=' + pro + '&center=' + loc;
                            console.log(e.target.name);
                            var productivity_bar_graph ='/api/chart_data/?';
                                                 var packet_clicked = e.target.series.name;
                                                 var is_exist = packet_clicked.indexOf('&');
                                                 if (is_exist > 0){
                                                    packet_clicked = packet_clicked.replace(' & ',' and ')
                                                 }

                            var dates_list = self.get_date();
                            //var dates_list = [self.start,self.end];
                            $http.get( productivity_bar_graph + 'packet=' + packet_clicked + '&date=' + e.target.category
                             + '&type=' + 'Production Chart'+addition).success(
                            function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    var proj = data.result.project;
                                    var pro_drill = data.result.table_headers;
                                    var chart_type = data.result.type;
                                    self.fields_list_drilldown = pro_drill;
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                                }
                            }
                            });
                            angular.extend(self.chartOptions17, {
                            xAxis: {
                                categories: self.high_data_gener[0].data.date,
                            },
                            series: self.high_data_gener[0].volume_graphs.bar_data
                            });
                            angular.extend(self.chartOptions17.plotOptions.series.point.events,{
                            select: function(e) {
                            var chart_name = 'volume_bar_graph';
                            var is_drill = self.list_object[chart_name].is_drilldown;
                            if (is_drill){
                            var addition = '&project=' + pro + '&center=' + loc;
                            console.log(e.target.name);
                            var productivity_bar_graph ='/api/chart_data/?';
                            var dates_list = self.get_date();
                            $http.get( productivity_bar_graph + 'packet=' + e.target.series.name + '&date=' + e.target.category
                             + '&type=' + 'Production Chart'+addition).success(
                            function(data,  status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    self.fields_list_drilldown = self.list_object_drilldown[data.result.type];
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                                }
                            }
                            });
                            angular.extend(self.chartOptions18, {
                                xAxis: {
                                    categories: self.high_data_gener[0].data.date,
                                    title: {
                                        text: '',
                                    }
                                },
                                plotOptions: {
                                    series : {
                                        allowPointSelect: true,
                                        cursor: 'pointer',
                                        point: {
                                            events:{
                                             select: function(e) {
                                             var chart_name = 'volume_productivity_graph';
                                             var is_drill = self.list_object[chart_name].is_drilldown;
                                             if (is_drill){ 
                                             var addition = '&project=' +pro + '&center=' +loc;
                                             console.log(e.target.series.name);
                                             var productivity_graph ='/api/chart_data/?'
                                             var packet_clicked = e.target.series.name;
                                             var is_exist = packet_clicked.indexOf('&');
                                             if (is_exist > 0){
                                                packet_clicked = packet_clicked.replace(' & ',' and ')
                                             }
                            $http.get( productivity_graph+ 'packet=' + packet_clicked + '&date=' + e.target.category +
                            '&type=' + 'Production Trends' + addition).success(
                            function(data, status)
                                {

                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    self.fields_list_drilldown = self.list_object_drilldown[data.result.type];
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                                }
                        }
                    }
                    }
                },
                bar: {
                 dataLabels: {
                 enabled: true
                 }
                }
               },
               series: self.high_data_gener[0].volume_graphs.line_data
             });
                            angular.extend(self.chartOptions5,{
                                series: [{
                                    name: '',
                                    colorByPoint: true,
                                    cursor: 'pointer',
                                    data: self.high_data_gener[0].internal_errors_types
                                }]
                            });
                            angular.extend(self.chartOptions5.plotOptions.pie.point.events,{
                            select: function(e) {
                            var chart_name = 'internal_error_accuracy_pie';
                            var is_drill = self.list_object[chart_name].is_drilldown;
                            if (is_drill){
                            var addition = '&project=' + pro + '&center=' + loc;
                            console.log(e.target.name);
                            var packet_clicked = e.target.name;
                            var is_exist = packet_clicked.indexOf('&');
                            if (is_exist > 0){
                                packet_clicked = packet_clicked.replace(' & ',' and ')
                            }
                            var internal_bar_graph ='/api/chart_data/?';
                            var dates_list = self.get_date();
                            //var dates_list = [self.start,self.end];
                            $http.get( internal_bar_graph + 'packet=' + packet_clicked + '&from=' + dates_list[0] + '&to=' + dates_list[1]
                             + '&type=' + 'Internal_Bar_Pie' + addition).success(
                            function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    var proj = data.result.project;
                                    var pro_drill = drilldown_config[proj];
                                    var chart_type = data.result.type;
                                    self.fields_list_drilldown = pro_drill[chart_type];
                                    //self.fields_list_drilldown = self.list_object_drilldown[data.result.type];
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                                }
                            }
                            });
                            angular.extend(self.chartOptions5_2,{
                                series: [{
                                    name: '',
                                    colorByPoint: true,
                                    cursor: 'pointer',
                                    data: self.high_data_gener[0].external_errors_types
                                }]
                            });
                            angular.extend(self.chartOptions5_2.plotOptions.pie.point.events,{
                            select: function(e) {
                            var chart_name = 'external_error_accuracy_pie';
                            var is_drill = self.list_object[chart_name].is_drilldown;
                            if (is_drill){
                            var addition = '&project=' + pro + '&center=' + loc;
                            console.log(e.target.name);
                            var external_bar_graph ='/api/chart_data/?';
                            var dates_list = self.get_date();
                            var packet_clicked = e.target.name;
                            var is_exist = packet_clicked.indexOf('&');
                            if (is_exist > 0){
                                packet_clicked = packet_clicked.replace(' & ',' and ')
                            }
                            //var dates_list = [self.start,self.end];
                            $http.get( external_bar_graph + 'packet=' + packet_clicked + '&from=' + dates_list[0] + '&to=' + dates_list[1]
                             + '&type=' + 'External_Bar_Pie'+ addition).success(
                            function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    var proj = data.result.project;
                                    var pro_drill = drilldown_config[proj];
                                    var chart_type = data.result.type;
                                    self.fields_list_drilldown = pro_drill[chart_type];
                                    //self.fields_list_drilldown = self.list_object_drilldown[data.result.type];
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                                }
                            }
                            });
                            angular.extend(self.chartOptions4.yAxis.title,{
                                text: ''
                            });
                            angular.extend(self.chartOptions4.plotOptions.series.point.events,{
                            select: function(e) {
                            var chart_name = 'internal_error_accuracy';
                            var is_drill = self.list_object[chart_name].is_drilldown;
                            if (is_drill){
                            var addition = '&project=' + pro + '&center=' + loc;
                            console.log(e.target.name);
                            var internal_bar_graph ='/api/chart_data/?';
                            var dates_list = self.get_date();
                            //var dates_list = [self.start,self.end];
                            var packet_clicked = e.target.name;
                            var is_exist = packet_clicked.indexOf('&');
                            if (is_exist > 0){
                                packet_clicked = packet_clicked.replace(' & ',' and ')
                            }
                            $http.get( internal_bar_graph + 'packet=' + packet_clicked + '&from=' + dates_list[0] + '&to=' + dates_list[1]
                             + '&type=' + 'Internal Accuracy'+addition).success(
                            function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    var proj = data.result.project;
                                    var pro_drill = data.result.table_headers;
                                    var chart_type = data.result.type;
                                    self.fields_list_drilldown = pro_drill;
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                                }
                            }
                            });
                            angular.extend(self.chartOptions4,{
              series: [{
                 name: 'accuracy',
                 cursor: 'pointer',
                 colorByPoint: true,
                    data: self.high_data_gener[0].internal_accuracy_graph
             }]
             });
                                         angular.extend(self.chartOptions6.yAxis.title,{
                                text: ''
                            });
                            angular.extend(self.chartOptions4.yAxis,{
                                min:result.result.int_min_value,
                                max:result.result.int_max_value
                            });
                            angular.extend(self.chartOptions6.plotOptions.series.point.events,{
                select: function(e) {
                var chart_name = 'external_error_accuracy';
                var is_drill = self.list_object[chart_name].is_drilldown;
                if (is_drill){
                var addition = '&project=' + pro + '&center=' + loc;
                        console.log(e);
                            var external_bar_graph ='/api/chart_data/?';
                            var packet_clicked = e.target.name;
                            var is_exist = packet_clicked.indexOf('&');
                            if (is_exist > 0){
                                packet_clicked = packet_clicked.replace(' & ',' and ')
                            }
                            var dates_list = self.get_date();
                            //var dates_list = [self.start,self.end];
                            $http.get( external_bar_graph + 'packet=' + packet_clicked + '&from=' + dates_list[0] + '&to=' + dates_list[1]
                             + '&type=' + 'External Accuracy' + addition).success(
                            function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    var proj = data.result.project;
                                    var pro_drill = data.result.table_headers;
                                    var chart_type = data.result.type;
                                    self.fields_list_drilldown = pro_drill;
                                    //self.fields_list_drilldown = self.list_object_drilldown[data.result.type];
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                                }
                        }
              });
                            angular.extend(self.chartOptions6,{
              series: [{
                 name: 'accuracy',
                 colorByPoint: true,
                 cursor: 'pointer',
                    data: self.high_data_gener[0].external_accuracy_graph
             }]
             });
                            angular.extend(self.chartOptions6.yAxis,{
                                min:result.result.ext_min_value,
                                max:result.result.ext_max_value
                            });
                            angular.extend(self.chartOptions15, {
                                xAxis: {
                                    categories: self.high_data_gener[0].data.date,
                                    title: {
                                        text: '',
                                    }
                                },
                                plotOptions: {
                                    series : {
                                        allowPointSelect: true,
                                    },
                                    bar: {
                                        dataLabels: {
                                            enabled: true
                                        }
                                    }
                                },
                                series: self.high_data_gener[0].original_utilization_graph
                            });
                            angular.extend(self.chartOptions15_2, {
                                xAxis: {
                                    categories: self.high_data_gener[0].data.date,
                                    title: {
                                        text: '',
                                    }
                                },
                                plotOptions: {
                                    series : {
                                        allowPointSelect: true,
                                    },
                                    bar: {
                                        dataLabels: {
                                            enabled: true
                                        }
                                    }
                                },
                                series: self.high_data_gener[0].utilization_work_packet_details
                            });
                            angular.extend(self.chartOptions16, {
                                xAxis: {
                                    categories: self.high_data_gener[0].data.date,
                                    title: {
                                        text: '',
                                    }
                                },
                                plotOptions: {
                                    series : {
                                        allowPointSelect: true,
                                    },
                                    bar: {
                                        dataLabels: {
                                            enabled: true
                                        }
                                    }
                                },
                                series: self.high_data_gener[0].fte_calc_data.work_packet_fte
                            });
                            angular.extend(self.chartOptions16_2, {
                                xAxis: {
                                    categories: self.high_data_gener[0].data.date,
                                    title: {
                                        text: '',
                                    }
                                },
                                plotOptions: {
                                    series : {
                                        allowPointSelect: true,
                                    },
                                    bar: {
                                        dataLabels: {
                                            enabled: true
                                        }
                                    }
                                },
                                series: self.high_data_gener[0].fte_calc_data.total_fte
                            });

            }
            self.get_date = function(){
                var dateEntered = document.getElementById('select').value;
                dateEntered = dateEntered.replace(' to ','to');
                var from = dateEntered.split('to')[0].replace(' ','');
                var to = dateEntered.split('to')[1].replace(' ','');
                return [from,to];
            };
            self.click = function(start,end){
                self.start = start.format('YYYY-MM-DD');
                self.end = end.format('YYYY-MM-DD');
                self.showLoading();
                //var dates_list = self.get_date();
                var dates_list = [self.start,self.end];
                var wor_pac = document.getElementById("0");
                var sub_pac = document.getElementById("1");
                var sub_pro = document.getElementById("2");
                if (wor_pac === null){
                    self.wor_pac_sel_two = 'undefined';
                }
                else {
                    self.wor_pac_sel_two = wor_pac.value;
                }
                if (sub_pac === null){
                    self.sub_pac_sel_two = 'undefined';
                }
                else {
                    self.sub_pac_sel_two = sub_pac.value;
                }
                if (sub_pro === null){
                    self.sub_pro_sel_two = 'undefined';
                }
                else {
                    self.sub_pro_sel_two = sub_pro.value;
                }
                if ((wor_pac.length >= 2) && (sub_pac.length > 1)){ 
                    self.sub_pro_sel_two = wor_pac.value;
                    self.sub_pac_sel_two = sub_pro.value;
                    self.wor_pac_sel_two = sub_pac.value;
                }
                else if ((wor_pac.length > 1) && (sub_pac.length > 1)){
                    self.sub_pro_sel_two = 'undefined';
                    self.sub_pac_sel_two = sub_pac.value;
                    self.wor_pac_sel_two = wor_pac.value;
                }
                else if ((wor_pac.length ==2) && (sub_pac.length == 1)){
                    self.sub_pro_sel_two = wor_pac.value;
                    self.sub_pac_sel_two = sub_pro.value;
                    self.wor_pac_sel_two = sub_pac.value;
                }
                else
                {
                    self.sub_pro_sel_two = 'undefined';
                    self.sub_pac_sel_two = 'undefined';
                    self.wor_pac_sel_two = wor_pac.value;
                }

                //self.wor_pac_sel_two = document.getElementById("0").value;
                //self.sub_pac_sel_two = document.getElementById("1").value;
                //self.sub_pro_sel_two = 'undefined';
                self.packet_clicked = self.wor_pac_sel_two;
                var is_exist = self.packet_clicked.indexOf('&');
                if (is_exist > 0){
                    self.packet_clicked = self.packet_clicked.replace(' & ',' and ')
                }
                var final_work =  '&sub_project=' + self.sub_pro_sel_two + '&sub_packet=' + self.sub_pac_sel_two + '&work_packet=' + self.packet_clicked;
                var from_to_data = from_to + 'from=' + dates_list[0] + '&to=' + dates_list[1] + '&project=' + self.project
                         + '&center=' + self.location + '&type=' + 'day' + final_work;
                $('.day').addClass('active');
                $('.day').siblings().removeClass('active');

                /*var from_to_data = from_to + 'from=' + dates_list[0] + '&to=' + dates_list[1] + '&project=' + self.project
                         + '&center=' + self.location + '&type=' + self.day_type;*/
                $http({method:"GET", url:from_to_data}).success(function(result){
                            $('#select').val(self.start + ' to ' + self.end)
                            self.sel_type = result.result.days_type;
                            if (self.sel_type === 'week'){
                                $('.week').addClass('active');
                                $('.week').siblings().removeClass('active');
                            }
                            if (self.sel_type === 'month'){
                                $('.month').addClass('active');
                                $('.month').siblings().removeClass('active');
                            }
                            if (self.sel_type === 'day'){
                                $('.day').addClass('active');
                                $('.day').siblings().removeClass('active');
                            }
                            self.chart_render(result,self.project,self.location);
                         });
            }
            self.update_one = function(index,selected_name){
            var sub_pro = self.sel_pack[0];
            var sub_pac = self.sel_pack[1];
            var wor_pac = self.sel_pack[2];
            var final_work =  '&sub_project=' + sub_pro + '&sub_packet=' + sub_pac + '&work_packet=' + wor_pac
            var dateEntered = document.getElementById('select').value
            dateEntered = dateEntered.replace(' to ','to');
            var from = dateEntered.split('to')[0].replace(' ','');
            var to = dateEntered.split('to')[1].replace(' ','');
            var placeholder = ''
            var from_to_data = from_to + 'from=' + from + '&to=' + to + '&project=' + self.project
                    + '&center=' + self.location + '&type=' + self.day_type  + final_work;

            $http({method:"GET", url:from_to_data}).success(function(result){
                self.high_data_gener = [];
                var final_data_gener = result.result;
                self.high_data_gener.push(final_data_gener);
                            angular.extend(self.chartOptions, {
               xAxis: {
                 categories: self.high_data_gener[0].data.date,
                 title: {
                  text: '',
                 }
               },
               plotOptions: {
                series : {
                    allowPointSelect: true,
                    point: {
                        events:{
                            select: function(e) {
                            console.log(e.target.series.name);
                            var productivity_graph ='/api/chart_data/?'
                            $http.get( productivity_graph+ 'packet=' + e.target.series.name + '&date=' + e.target.category).success(
                            function(data, status)
                                {
                                    $('#myModal').modal('show');
                                    var names_list =  data.result;
                                    self.names = names_list;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});

                        }
                    }
                    }
                },
                bar: {
                 dataLabels: {
                 enabled: true
                 }
                }
               },
               series: self.high_data_gener[0].productivity_data
             });

                            angular.extend(self.chartOptions9_2.yAxis,{
                                min:result.result.min_external_time_line,
                                max:result.result.max_external_time_line
                            });
                            angular.extend(self.chartOptions9_2, {
                            xAxis: {
                                categories: self.high_data_gener[0].data.date,
                                title: {
                                    text: '',
                                }
                            },
                            series: self.high_data_gener[0].external_time_line
                            });
                            angular.extend(self.chartOptions9.yAxis,{
                                min:result.result.min_internal_time_line,
                                max:result.result.max_internal_time_line
                            });
                            angular.extend(self.chartOptions9, {
                            xAxis: {
                                categories: self.high_data_gener[0].data.date,
                                title: {
                                    text: '',
                                }
                            },
                            series: self.high_data_gener[0].internal_time_line
                            });
                            angular.extend(self.chartOptions19, {
                            xAxis: {
                                categories: self.high_data_gener[0].data.date,
                                title: {
                                    text: '',
                                }
                            },
                            series: self.high_data_gener[0].original_productivity_graph
                            });
                            angular.extend(self.chartOptions20, {
                            xAxis: {
                                categories: self.high_data_gener[0].data.date,
                                title: {
                                    text: '',
                                }
                            },
                            series: self.high_data_gener[0].internal_pareto_graph_data
                            });

                            angular.extend(self.chartOptions21, {
                            xAxis: {
                                categories: self.high_data_gener[0].data.date,
                                title: {
                                    text: '',
                                }
                            },
                            series: self.high_data_gener[0].external_pareto_graph_data
                            });

                            angular.extend(self.chartOptions10, {
                            xAxis: {
                                categories: self.high_data_gener[0].data.date
                            },
                            series: self.high_data_gener[0].productivity_data
                            });
                            angular.extend(self.chartOptions4.yAxis.title,{
                                text: ''
                            });
                            angular.extend(self.chartOptions4.plotOptions.series.point.events,{
                select: function(e) {
                        console.log(e);
                        $("#perc_hello").html(e.target.name);
                        $("#perc_temp").html(e.target.y);
                        $('#percent_graph').modal('show');
                        }
              });
                            angular.extend(self.chartOptions4,{
              series: [{
                 name: 'accuracy',
                 colorByPoint: true,
                    data: self.high_data_gener[0].internal_accuracy_graph
             }]
             });
                            angular.extend(self.chartOptions4.yAxis,{
                                min:result.result.int_min_value,
                                max:result.result.int_max_value
                            })
                            angular.extend(self.chartOptions5,{
                                series: [{
                                    name: '',
                                    colorByPoint: true,
                                    data: self.high_data_gener[0].internal_errors_types
                                }]
                            });
                            angular.extend(self.chartOptions5_2,{
                                series: [{
                                    name: '',
                                    colorByPoint: true,
                                    data: self.high_data_gener[0].external_errors_types
                                }]
                            });
angular.extend(self.chartOptions18, {
                                xAxis: {
                                    categories: self.high_data_gener[0].data.date,
                                    title: {
                                        text: '',
                                    }
                                },
                                plotOptions: {
                                    series : {
                                        allowPointSelect: true,
                                        cursor: 'pointer',
                                        point: {
                                            events:{
                                             select: function(e) {

                                             var addition = '&project=' +pro + '&center=' +loc;
                                             console.log(e.target.series.name);
                                             var productivity_graph ='/api/chart_data/?'
                                             var packet_clicked = e.target.series.name;
                                             var is_exist = packet_clicked.indexOf('&');
                                             if (is_exist > 0){
                                                packet_clicked = packet_clicked.replace(' & ',' and ')
                                             }
                            $http.get( productivity_graph+ 'packet=' + packet_clicked + '&date=' + e.target.category +
                            '&type=' + 'Production Trends' + addition).success(
                            function(data, status)
                                {

                                    $('#myModal').modal('show');
                                    self.names = data.result.data;
                                    self.fields_list_drilldown = self.list_object_drilldown[data.result.type];
                                    self.chart_type = data.result.type;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});

                        }
                    }
                    }
                },
                bar: {
                 dataLabels: {
                 enabled: true
                 }
                }
               },
               series: self.high_data_gener[0].productivity_data
             });
                            angular.extend(self.chartOptions6.yAxis.title,{
                                text: ''
                            });
                            angular.extend(self.chartOptions6.plotOptions.series.point.events,{
                                select: function(e) {
                        console.log(e);
                        $("#perc_hello").html(e.target.name);
                        $("#perc_temp").html(e.target.y);
                        $('#percent_graph').modal('show');
                        }
                            });
                            angular.extend(self.chartOptions6,{
              series: [{
                 name: 'accuracy',
                 colorByPoint: true,
                    data: self.high_data_gener[0].external_accuracy_graph
             }]
             });
                            angular.extend(self.chartOptions6.yAxis,{
                                min:result.result.ext_min_value,
                                max:result.result.ext_max_value
                            });
                            });
            }

            $http({method:"GET", url:drop_down_link}).success(function(result){
                angular.extend(self.packet_hierarchy_list, result.result.level);
             })

            self.chartOptions = {
                chart : {
                 backgroundColor: "transparent"
                },
                               yAxis: {
                gridLineColor: 'a2a2a2',
                min: 0,
                title: {
                 text: '',
                 align: 'high'
                },
                labels: {
                 overflow: 'justify'
                }
               },

               tooltip: {
                valueSuffix: ''
               },
               credits: {
                enabled: false
               },
            };
            self.chartOptions10 = {
            chart: {
                type: 'column',
                backgroundColor: "transparent"
             },
            title: {
                text: ''
            },
            subtitle: {
                text: ''
            },
            yAxis: {
                gridLineColor: 'a2a2a2',
                min: 0,
                title: {
                    text: ''
                }
            },
            plotOptions:{
                series:{
                    allowPointSelect: true,
                    cursor: 'pointer',
                point: {
                    events:{
                    }
                }
                }
            }
            };
            self.chartOptions9 = {
                chart : {
                 backgroundColor: "transparent"
                },
                               yAxis: {
                gridLineColor: 'a2a2a2',
                min: 0,
                title: {
                 text: '',
                 align: 'high'
                },
                labels: {
                 overflow: 'justify'
                }
               },

               tooltip: {
                valueSuffix: ''
               },
               credits: {
                enabled: false
               },
            };
            self.chartOptions9_2 = {
                chart : {
                 backgroundColor: "transparent"
                },
                               yAxis: {
                gridLineColor: 'a2a2a2',
                min: 0,
                title: {
                 text: '',
                 align: 'high'
                },
                labels: {
                 overflow: 'justify'
                }
               },

               tooltip: {
                valueSuffix: ''
               },
               credits: {
                enabled: false
               },
            };
            self.chartOptions4 = {
            chart: {
                type: 'column',
                backgroundColor: "transparent"
             },
            title: {
                text: ''
            },
            subtitle: {
                text: ''
            },
            xAxis: {
                type: 'category'
            },
            legend: {
                enabled: false
            },
            yAxis: {
                min:'',
                max:'',
                gridLineColor: 'a2a2a2',
                title: {
                    text: ''
                }
            },
            plotOptions:{
                series:{
                    allowPointSelect: true,
                point: {
                    events:{
                    }
                },
                dataLabels: {
                enabled: true,
                }
                }
            },

            };
            self.chartOptions5 = {
                chart: {
                    backgroundColor: "transparent",
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie'
                  },
                title: {
                    text: ''
                  },
                tooltip: {
                    pointFormat: '<b>{point.y}</b>'
                  },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        point: {
                           events:{
                           }
                        },
                        cursor: 'pointer',
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b>: {point.y} ',
                            style: {
                                color:(Highcharts.theme && Highcharts.theme.background2) || '#EEE'
                               }
                            }
                        }
                    },
                };
            self.chartOptions5_2 = {
                chart: {
                    backgroundColor: "transparent",
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie'
                  },
                title: {
                    text: ''
                  },
                tooltip: {
                    pointFormat: '<b>{point.y}</b>'
                  },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        point: {
                           events:{
                           }
                        },
                        cursor: 'pointer',
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b>: {point.y} ',
                            style: {
                                color:(Highcharts.theme && Highcharts.theme.background2) || '#EEE'
                               }
                            }
                        }
                    },
                };
            self.chartOptions6 = {
            chart: {
                type: 'column',
                backgroundColor: "transparent"
             },
            title: {
                text: ''
            },
            subtitle: {
                text: ''
            },
            xAxis: {
                type: 'category'
            },
            legend: {
                enabled: false
            },
            yAxis: {
                min:'',
                max:'',
                gridLineColor: 'a2a2a2',
                title: {
                    text: ''
                }
            },
            plotOptions:{
                series:{
                    allowPointSelect: true,
                point: {
                    events:{
                    }
                },
                dataLabels: {
                    enabled: true,
                }
                }
            },

            };
            self.chartOptions15 = {
                chart : {
                 backgroundColor: "transparent"
                },
                               yAxis: {
                gridLineColor: 'a2a2a2',
                min: 0,
                title: {
                 text: '',
                 align: 'high'
                },
                labels: {
                 overflow: 'justify'
                }
               },

               tooltip: {
                valueSuffix: ''
               },
               credits: {
                enabled: false
               },
            };
            self.chartOptions15_2 = {
                chart : {
                 backgroundColor: "transparent"
                },
                               yAxis: {
                gridLineColor: 'a2a2a2',
                min: 0,
                title: {
                 text: '',
                 align: 'high'
                },
                labels: {
                 overflow: 'justify'
                }
               },

               tooltip: {
                valueSuffix: ''
               },
               credits: {
                enabled: false
               },
            };
            self.chartOptions16 = {
                chart : {
                 backgroundColor: "transparent"
                },
                               yAxis: {
                gridLineColor: 'a2a2a2',
                min: 0,
                title: {
                 text: '',
                 align: 'high'
                },
                labels: {
                 overflow: 'justify'
                }
               },

               tooltip: {
                valueSuffix: ''
               },
               credits: {
                enabled: false
               },
            };
            self.chartOptions16_2 = {
                chart : {
                 backgroundColor: "transparent"
                },
                               yAxis: {
                gridLineColor: 'a2a2a2',
                min: 0,
                title: {
                 text: '',
                 align: 'high'
                },
                labels: {
                 overflow: 'justify'
                }
               },

               tooltip: {
                valueSuffix: ''
               },
               credits: {
                enabled: false
               },
            };
            self.chartOptions17 = {
            chart: {
                type: 'column',
                backgroundColor: "transparent"
             },
            title: {
                text: ''
            },
            subtitle: {
                text: ''
            },
            yAxis: {
                gridLineColor: 'a2a2a2',
                min: 0,
                title: {
                    text: ''
                }
            },
            plotOptions:{
                series:{
                    allowPointSelect: true,
                    cursor: 'pointer',
                point: {
                    events:{
                    }
                }
                }
            }
            };
            self.chartOptions18 = {
                chart : {
                 backgroundColor: "transparent"
                },
                               yAxis: {
                gridLineColor: 'a2a2a2',
                min: 0,
                title: {
                 text: '',
                 align: 'high'
                },
                labels: {
                 overflow: 'justify'
                }
               },

               tooltip: {
                valueSuffix: ''
               },
               credits: {
                enabled: false
               },
            };
            self.chartOptions19 = {
                chart : {
                 backgroundColor: "transparent"
                },
                               yAxis: {
                gridLineColor: 'a2a2a2',
                min: 0,
                title: {
                 text: '',
                 align: 'high'
                },
                labels: {
                 overflow: 'justify'
                }
               },

               tooltip: {
                valueSuffix: ''
               },
               credits: {
                enabled: false
               },
            };

            self.chartOptions20 = {
                chart: {
            zoomType: 'xy',
            backgroundColor: "transparent",

        },
        xAxis: [{

            crosshair: true,
            color:'a2a2a2',
        }],
        yAxis: [{
            gridLineWidth: 0,
            minorGridLineWidth: 0,
            gridLineColor: 'a2a2a2',

            labels: {
                color: 'a2a2a2',
                format: '{value}',
            },
            title: {
                text: 'Error Accuracy',
                color:'a2a2a2',
            }
        }, { // Secondary yAxis
            gridLineWidth: 0,
            minorGridLineWidth: 0,
            title: {
                text: 'Error Count',
                color:'a2a2a2',
            },
            labels: {
                color: 'a2a2a2',
                format: '{value} ',
            },
            opposite: true
        },],
        tooltip: {
            shared: true
        },
        legend: {

              itemStyle: {
                    'color' : '#717171',
               } 
        },
    }


    self.chartOptions21 = {
                chart: {
            zoomType: 'xy',
            backgroundColor: "transparent",

        },
        xAxis: [{

            crosshair: true,
            color:'a2a2a2',
        }],
        yAxis: [{
            gridLineWidth: 0,
            minorGridLineWidth: 0,
            gridLineColor: 'a2a2a2',

            labels: {
                color: 'a2a2a2',
                format: '{value}',
            },
            title: {
                text: 'Error Accuracy',
                color:'a2a2a2',
            }
        }, { // Secondary yAxis
            gridLineWidth: 0,
            minorGridLineWidth: 0,
            title: {
                text: 'Error Count',
                color:'a2a2a2',
            },
            labels: {
                color: 'a2a2a2',
                format: '{value} ',
            },
            opposite: true
        },],
        tooltip: {
            shared: true
        },
        legend: {
               itemStyle: {
                    'color' : '#717171',
               }
        },
    }


            //self.hideLoading();
            self.names;
            self.names_2;
            self.first;
            self.last;
            self.location = '';
            self.project = '';
            self.packet_count = '';
            self.list_object = '';
            self.layout_list = '';
            self.packet_hierarchy_list = [];
            self.day_type = 'day';
            self.useful_layout = [];
            self.sel_pack = [];
            self.drop_list = [];
            self.top_employee_details = '';
            self.global_packet_values = '';
            self.firstDate;
            self.lastDate;
            self.start;
            self.end;
            }],

            "bindings": {

              "hideLoading": "&",
              "showLoading": "&",
              "updateState": "&",
              "selectedValue": "=",
              "selectDropdown": "&",
              "tabData": "<"
            }
         });

}(window.angular));
