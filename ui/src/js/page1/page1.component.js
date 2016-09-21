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

             $http({method:"GET", url:project}).success(function(result){
                if(result.result.role === 'customer'){
                    var pro_cen_nam = result.result.list[1]
                    self.layout_list = result.result.lay[0][pro_cen_nam]
                    self.list_object = {
                        "productivity_chart": {
                            'title': 'Productivity Chart',
                            'id': 1,
                            'col': 12,
                            'api': '',
                            'opt': self.chartOptions
                        },
                        "internal_error_accuracy": {
                            'title': 'Internal Accuracy Graph',
                            'id': 2,
                            'col': 6,
                            'api': '',
                            'opt': self.chartOptions4
                        },
                        "external_error_accuracy": {
                            'title': 'External Accuracy Graph',
                            'id': 3,
                            'col': 6,
                            'api': '',
                            'opt': self.chartOptions6
                        }
                    };
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
                    /*var from_to_data = from_to + 'from=' + lastDate + '&to=' + firstDate + '&project=' + self.project
                         + '&center=' + self.location;*/

                     var from_to_data = from_to + 'from=' + '2016-7-21' + '&to=' + '2016-7-27' + '&project=' + self.project
                         + '&center=' + self.location + '&type=' + self.day_type;
                    $http({method:"GET", url:from_to_data}).success(function(result){
                        self.packet_count = result.result.productivity_data.length;
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
                            angular.extend(self.chartOptions4.yAxis.title,{
                                text: 'In Percentage'
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


                                         angular.extend(self.chartOptions6.yAxis.title,{
                                text: 'In Percentage'
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

                            /*angular.extend(self.chartOptions6,{
        xAxis: {
            categories: self.high_data_gener[0].extr_err_accuracy.extr_err_name
        },
        series: [{
            name: 'Accuracy',
            data: self.high_data_gener[0].extr_err_accuracy.extr_err_perc
        },]

              });*/
                         });
                }
             })
             console.log(firstDate);
             console.log(lastDate);
             self.updateState();
             console.log('Hello from page1 yesh');
             $scope.options = self.tabData;

             var unWatch;

             this.$onInit = function () {
                unWatch = $scope.$watch(function(scope) {
                    return scope.options.state;
                },
                function(newVal){
                    if (newVal.state) {
                        self.location = newVal.state.split(' - ')[0] + ' - ';
                        self.project = newVal.state.split(' - ')[1] + ' - ';
                        var from_to_data = from_to + 'from=' + '2016-7-21' + '&to=' + '2016-7-27' + '&project=' + self.project
                         + '&center=' + self.location;
                        self.tabData.state = JSON.parse("{}");
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
                            angular.extend(self.chartOptions3,{
              series: [{
            colorByPoint: true,
            name: 'error count',
            data: self.high_data_gener[0].volumes_data.volume_new_data,
            dataLabels: {
                enabled: true,
                rotation: -90,
                color: '#FFFFFF',
                align: 'right',
                y: 10, // 10 pixels down from the top
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        }]
              });
                            angular.extend(self.chartOptions4.yAxis.title,{
                                text: 'In Percentage'
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
                            angular.extend(self.chartOptions5_2,{
                series: [{
                        name: 'Brands',
                        colorByPoint: true,
                        data: self.high_data_gener[0].extrn_error_count
                    }]
             });
                            angular.extend(self.chartOptions5,{
                series: [{
                        name: 'Brands',
                        colorByPoint: true,
                        data: self.high_data_gener[0].internal_error_count
                    }]
             });
                            /*angular.extend(self.chartOptions6,{
        xAxis: {
            categories: self.high_data_gener[0].extr_err_accuracy.extr_err_name
        },
        series: [{
            name: 'Accuracy',
            data: self.high_data_gener[0].extr_err_accuracy.extr_err_perc
        },]

              });*/
                         });
                    }
                });
             };
             this.$onDestroy = function () {
               return unWatch && unWatch();
             }
             /*$http({method:"GET", url:def_display}).success(function(result){
                cosole.log('Def');
             });*/
             var from_to_data = from_to + 'from=' + lastDate + '&to=' + firstDate + '&project=' + self.project
                         + '&center=' + self.location;


                self.first = firstDate;
                self.last = lastDate;



            self.dateType = function(key){
                self.day_type = key;
                self.high_data = [];
                var dateEntered = document.getElementById('select').value
                var from = dateEntered.split('to')[0].replace(' ','');
                var to = dateEntered.split('to')[1].replace(' ','');
                var from_to_data = from_to + 'from=' + from + '&to=' + to + '&project=' + self.project
                         + '&center=' + self.location + '&type=' + self.day_type;
                console.log(from_to_data);
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
                            angular.extend(self.chartOptions4.yAxis.title,{
                                text: 'In Percentage'
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
                                         angular.extend(self.chartOptions6.yAxis.title,{
                                text: 'In Percentage'
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

                            /*angular.extend(self.chartOptions6,{
        xAxis: {
            categories: self.high_data_gener[0].extr_err_accuracy.extr_err_name
        },
        series: [{
            name: 'Accuracy',
            data: self.high_data_gener[0].extr_err_accuracy.extr_err_perc
        },]

              });*/
                         });
            }

            self.chartOptions = {
                chart : {
                 backgroundColor: "transparent"
                },
                               yAxis: {
                gridLineColor: 'a2a2a2',
                min: 0,
                title: {
                 text: 'per day achieved',
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
            yAxis: {
                gridLineColor: 'a2a2a2',
                title: {
                    text: 'In Percentage'
                }
            },
            plotOptions:{
                series:{
                    allowPointSelect: true,
                point: {
                    events:{
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
            yAxis: {
                gridLineColor: 'a2a2a2',
                title: {
                    text: 'In Percentage'
                }
            },
            plotOptions:{
                series:{
                    allowPointSelect: true,
                point: {
                    events:{
                    }
                }
                }
            },

            };
            /*self.chartOptions6 = {
                        title: {
            text: '',
            x: -20 //center
        },
        subtitle: {
            text: '',
            x: -20
        },
        yAxis: {
            title: {
                text: ''
            },
            gridLineColor: 'a2a2a2',
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: '°C'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
            };*/
            self.hideLoading();
            self.names;
            self.names_2;
            self.first;
            self.last;
            self.location = '';
            self.project = '';
            self.packet_count = '';
            self.list_object = '';
            self.layout_list = '';
            self.day_type = 'day';
            self.useful_layout = [];
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
