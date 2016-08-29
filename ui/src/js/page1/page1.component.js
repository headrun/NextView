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
                    self.location = pro_cen_nam.split('-')[0].replace(' ','') + ' - '
                    self.project = pro_cen_nam.split('-')[1].replace(' ','') + ' - '
                    /*var from_to_data = from_to + 'from=' + lastDate + '&to=' + firstDate + '&project=' + self.project
                         + '&center=' + self.location;*/
                     var from_to_data = from_to + 'from=' + '2016-7-21' + '&to=' + '2016-7-27' + '&project=' + self.project
                         + '&center=' + self.location;
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
                            angular.extend(self.chartOptions6,{
        xAxis: {
            categories: self.high_data_gener[0].extr_err_accuracy.extr_err_name
        },
        series: [{
            name: 'Accuracy',
            data: self.high_data_gener[0].extr_err_accuracy.extr_err_perc
        },]

              });
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
                            angular.extend(self.chartOptions6,{
        xAxis: {
            categories: self.high_data_gener[0].extr_err_accuracy.extr_err_name
        },
        series: [{
            name: 'Accuracy',
            data: self.high_data_gener[0].extr_err_accuracy.extr_err_perc
        },]

              });
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

              $http({method:"GET", url:from_to_data}).success(function(result){
                    self.high_data_pre = [];
                    var final_data = result.result;
                    console.log(final_data);
                    self.high_data_pre.push(final_data);
              angular.extend(self.chartOptions5_2,{
                series: [{
                        name: 'Brands',
                        colorByPoint: true,
                        data: [{
                            name: 'DF',
                            y: self.high_data[0].extrn_error_count.DF
                        }, {
                            name: 'DD',
                            y: self.high_data[0].extrn_error_count.DD,
                            sliced: true,
                            selected: true
                        }, {
                            name: 'GC',
                            y: self.high_data[0].extrn_error_count.GC
                        }, {
                            name: 'FES',
                            y: self.high_data[0].extrn_error_count.FES
                        }, {
                            name: 'Compliance',
                            y: self.high_data[0].extrn_error_count.Compliance
                        }, {
                            name: 'LLP',
                            y: self.high_data[0].extrn_error_count.LLP
                        }, {
                            name: 'MD',
                            y: self.high_data[0].extrn_error_count.MD
                        }, {
                            name: 'Charges',
                            y: self.high_data[0].extrn_error_count.Charges
                        }, {
                            name: 'Legal',
                            y: self.high_data[0].extrn_error_count.Legal
                        }, {
                            name: 'CC',
                            y: self.high_data[0].extrn_error_count.CC
                        }]
                    }]
             });
              angular.extend(self.chartOptions5,{
                series: [{
                        name: 'Brands',
                        colorByPoint: true,
                        data: [{
                            name: 'DF',
                            y: self.high_data_pre[0].error_count.DF
                        }, { 
                            name: 'DD',
                            y: self.high_data_pre[0].error_count.DD,
                            sliced: true,
                            selected: true 
                        }, { 
                            name: 'GC',
                            y: self.high_data_pre[0].error_count.GC
                        }, { 
                            name: 'FES',
                            y: self.high_data_pre[0].error_count.FES
                        }, { 
                            name: 'Compliance',
                            y: self.high_data_pre[0].error_count.Compliance
                        }, { 
                            name: 'LLP',
                            y: self.high_data_pre[0].error_count.LLP
                        }, { 
                            name: 'MD',
                            y: self.high_data_pre[0].error_count.MD
                        }, { 
                            name: 'Charges',
                            y: self.high_data_pre[0].error_count.Charges
                        }, { 
                            name: 'Legal',
                            y: self.high_data_pre[0].error_count.Legal
                        }, { 
                            name: 'CC',
                            y: self.high_data_pre[0].error_count.CC
                        }]
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
                    data: [{
                            name: 'DF',
                            y: self.high_data_pre[0].accuracy_graph.DF
                        }, { 
                            name: 'DD',
                            y: self.high_data_pre[0].accuracy_graph.DD,
                        }, {

                            name: 'GC',
                            y: self.high_data_pre[0].accuracy_graph.GC
                        }, {
                            name: 'FES',
                            y: self.high_data_pre[0].accuracy_graph.FES
                        }, {
                            name: 'Compliance',
                            y: self.high_data_pre[0].accuracy_graph.Compliance
                        }, {
                            name: 'LLP',
                            y: self.high_data_pre[0].accuracy_graph.LLP
                        }, {
                            name: 'MD',
                            y: self.high_data_pre[0].accuracy_graph.MD
                        }, {
                            name: 'Charges',
                            y: self.high_data_pre[0].accuracy_graph.Charges
                        }, {
                            name: 'Legal',
                            y: self.high_data_pre[0].accuracy_graph.Legal
                        }, {
                            name: 'CC',
                            y: self.high_data_pre[0].accuracy_graph.CC
                        }]

             }]
             });
              angular.extend(self.chartOptions3,{
              series: [{
            colorByPoint: true,
            name: 'error count',
            data: self.high_data_pre[0].volumes_data.volume_new_data,
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
              angular.extend(self.chartOptions, {
               xAxis: {
                 categories: self.high_data_pre[0].data.date,
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
               series: [{
                name: 'DD',
                data: self.high_data_pre[0].data.data.DD
                }, {
                name: 'DF',
                data: self.high_data_pre[0].data.data.DF
                }, {
                name: 'CC',
                data: self.high_data_pre[0].data.data.CC
                },{
                name: 'GC',
                data: self.high_data_pre[0].data.data.GC
                },{
                name: 'Compliance',
                data: self.high_data_pre[0].data.data.Compliance
                },{
                name: 'Legal',
                data: self.high_data_pre[0].data.data.Legal
                },{
                name: 'MD',
                data: self.high_data_pre[0].data.data.MD
                },{
                name: 'LLP',
                data: self.high_data_pre[0].data.data.LLP
                },{
                name: 'Charges',
                data: self.high_data_pre[0].data.data.Charges
                },{
                name: 'FES',
                data: self.high_data_pre[0].data.data.FES
                },
                ]
             });
              });


            self.check = function() {
                self.high_data = [];
                var dateEntered = document.getElementById('select').value
                var from = dateEntered.split('to')[0].replace(' ','');
                var to = dateEntered.split('to')[1].replace(' ','');
                var from_to_data = from_to + 'from=' + from + '&to=' + to + '&project=' + self.project
                         + '&center=' + self.location;

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
                            angular.extend(self.chartOptions6,{
        xAxis: {
            categories: self.high_data_gener[0].extr_err_accuracy.extr_err_name
        },
        series: [{
            name: 'Accuracy',
            data: self.high_data_gener[0].extr_err_accuracy.extr_err_perc
        },]

              });
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
            self.chartOptions3 = {
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
            type: 'category',
            labels: {
                rotation: -45,
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        },
        yAxis: {
            gridLineColor: 'a2a2a2',
            gridLineDashStyle: 'solid',
            min: 0,
            title: {
                text: 'total'
            }
        },
        legend: {
            enabled: false
        },
        plotOptions:{
            series:{
            allowPointSelect: true,
             point: {
                events:{
                    select: function(e) {
                    console.log(e);
                    $("#pwe_hello").html(e.target.name);
                    //$("#temp").html(e.target.y);
                    $("#pwe_temp").html(e.target.y);
                    $('#pwe_myModal').modal('show');
                    }
                }
             }
            }
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
               pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
               pie: {
                   allowPointSelect: true,
                   cursor: 'pointer',
                   dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.y} ',
                        style: {
                             //color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'white'
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
               pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
               pie: {
                   allowPointSelect: true,
                   cursor: 'pointer',
                   dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.y} ',
                        style: {
                             //color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'white'
                             color:(Highcharts.theme && Highcharts.theme.background2) || '#EEE'
                               }
                            }
                        }
                    },
            };
            self.chartOptions6 = {
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
            };
            self.hideLoading();
            self.names;
            self.names_2;
            self.first;
            self.last;
            self.location = '';
            self.project = '';

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
