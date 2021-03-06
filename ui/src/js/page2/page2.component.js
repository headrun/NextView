;(function (angular) {
  "use strict";

  angular.module("page2")
         .component("page2", {

           "templateUrl": "/js/page2/page2.html",
           "controller": ['$http',

           function ($http) {

             var self = this;
             var from_to = '/api/from_to/?'
             var error_api = '/api/error_board'
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
             //lastDate = '2016-7-1';
             //firstDate = '2016-7-14';

             console.log(firstDate);
             console.log(lastDate);

             $http.get(from_to + 'from=' + lastDate + '&to=' + firstDate).success(
                    function(data, status)
                    {
                        console.log('Sucess');
                    }).error(function(error){ console.log("error")});

             var from_to_data = from_to + 'from=' + lastDate + '&to=' + firstDate;

             $http({method:"GET", url:error_api}).success(function(result){
                    self.high_data_error = [];
                    self.high_data_error.push(result.result.error_count);
                    self.high_data_error.push(result.result.accuracy_graph);
                    console.log('Yesh');
                    /*angular.extend(self.chartOptions3,{
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
                text: 'errors'
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

        series: [{
            name: 'error count',
            data: self.high_data_error[0],
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

                    });*/
                    /*angular.extend(self.chartOptions4,{
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
                text: 'In percentage'
            }

        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
                allowPointSelect: true,
                point: {
                    events:{
                        select: function(e) {
                        console.log(e);
                        $("#perc_hello").html(e.target.name);
                    //$("#temp").html(e.target.y);
                        $("#perc_temp").html(e.target.y);
                        $('#percent_graph').modal('show');
                        }
                    }
                },
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                    format: '{point.y:.1f}%'
                }
            }
        },

        tooltip: {
            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
        },

        series: [{
            name: 'accuracy',
            colorByPoint: true,
            data: [{
                name: 'DF',
                y: self.high_data_error[1].DF

            }, {
                name: 'Compliance',
                y: self.high_data_error[1].Compliance

            }, {
                name: 'CC',
                y: self.high_data_error[1].CC

            }, {
                name: 'GC',
                y: self.high_data_error[1].GC

            }, {
                name: 'Charges',
                y: self.high_data_error[1].Charges
            }, {
                name: 'DF',
                y: self.high_data_error[1].DF

            }]
        }],
        drilldown: {
            series: [ ]
        }
                    });*/
        /*angular.extend(self.chartOptions4.yAxis.title,{
                text: 'errors'
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
                    y: self.high_data_error[1].DF
                }, {
                    name: 'DD',
                    y: self.high_data_error[1].DD
                }, {
                    name: 'CC',
                    y: self.high_data_error[1].CC
                }, {
                    name: 'GC',
                    y: self.high_data_error[1].GC
                } ]
             }]
             });*/


             });

             $http({method:"GET", url:yesterdays_data}).success(function(result){
                    self.high_data_yesterday = [];
                    self.high_data_yesterday.push(result.result);
                    console.log('Yesterday_data');
                    /*angular.extend(self.chartOptions5,{
                series: [{
                        name: 'Brands',
                        colorByPoint: true,
                        data: [{
                            name: 'DF',
                            y: 1
                        }, {
                            name: 'DD',
                            y: 0,
                            sliced: true,
                            selected: true
                        }, {
                            name: 'GC',
                            y: 1
                        }, {
                            name: 'FES',
                            y: 0
                        }, {
                            name: 'Compilance',
                            y: 6
                        }, {
                            name: 'LLP',
                            y: 0
                        }]
                    }]
             });*/
             });

             $http({method:"GET", url:from_to_data}).success(function(result){
                    self.high_data_pre = [];
                    var final_data = result.result;
                    console.log(final_data);
                    self.high_data_pre.push(final_data);
                    //console.log(self.high_data_pre);
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
                text: 'errors'
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

          angular.extend(self.chartOptions, {
               chart : {
                 backgroundColor: "transparent"
               },
               xAxis: {
                 categories: self.high_data_pre[0].data.date,
                 title: {
                  text: '',
                 }
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
                                    //console.log(data.result);
                                    /*$("#hello").html(data.result.emp_names +'</br>'+ data.result.work_packet_values+ '</br>' +e.target.y);*/
                                    $('#myModal').modal('show');
                                    var names_list =  data.result;
                                    self.names = names_list;
                                    console.log(self.names);
                                }).error(function(error){ console.log("error")});
                            //console.log(e.target.series.name);
                            //$("#hello").html(e.target.category);
                            //$("#temp").html(e.target.y);

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

               credits: {
                enabled: false
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
           angular.extend(self.chartOptions2, {
         chart: {
            type: 'bar',
            backgroundColor: "transparent"
        },
        title: {
            text: ''
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            gridLineColor: '#a2a2a2',
            categories: ["MD","LLP","CC","DD","Compliance","Legal","Charges","GC","FES"],
            title: {
                text: null
            }
        },
        yAxis: {
            gridLineColor: 'a2a2a2',
            min: 0,
            title: {
                text: 'total achieved',
                align: 'high'
            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            valueSuffix: ''
        },
       plotOptions: {
            series : {
                allowPointSelect: true,
                    point: {
                        events:{
                            select: function(e) {
                            console.log(e);
                            $("#wpp_hello").html(e.target.category);
                            $("#wpp_temp").html(e.target.y);
                            $('#workpacket_per').modal('show');
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
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -40,
            y: 80,
            floating: true,
            borderWidth: 1,
            //backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
            shadow: true
        },
        credits: {
            enabled: false
        },
        series: [{
            name: 'package',
            data: [self.high_data_pre[0].volumes_data.volume_values.MD, self.high_data_pre[0].volumes_data.volume_values.LLP,
            self.high_data_pre[0].volumes_data.volume_values.CC,self.high_data_pre[0].volumes_data.volume_values.DD,
            self.high_data_pre[0].volumes_data.volume_values.Compliance,self.high_data_pre[0].volumes_data.volume_values.Legal,
            self.high_data_pre[0].volumes_data.volume_values.Charges,self.high_data_pre[0].volumes_data.volume_values.GC,
            self.high_data_pre[0].volumes_data.volume_values.FES]
        }]
             });

            angular.extend(self.chartOptions3,{
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
                text: 'errors'
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
                    });

             /*$http({method:"GET", url:yesterdays_data}).success(function(result){
                    self.high_data_yesterday = [];
                    self.high_data_yesterday.push(result.result);
                    console.log('Yesterday_data');
                    angular.extend(self.chartOptions5,{
                    chart: {
                        plotBackgroundColor: null,
                        plotBorderWidth: null,
                        plotShadow: false,
                        type: 'pie'
                    },
                    title: {
                        text: 'yesterday data'
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
                                    color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                                }
                            }
                        }
                    },
                    series: [{
                        name: 'Brands',
                        colorByPoint: true,
                        data: [{
                            name: 'DF',
                            y: 146
                        }, {
                            name: 'DD',
                            y: 243,
                            sliced: true,
                            selected: true
                        }, {
                            name: 'GC',
                            y: 108
                        }, {
                            name: 'FES',
                            y: 247
                        }, {
                            name: 'Compilance',
                            y: 101
                        }, {
                            name: 'LLP',
                            y: 102
                        }]
                    }]

                    });

             });*/

            self.check = function() {
                self.high_data = [];
                var dateEntered = document.getElementById('select').value
                var from = dateEntered.split('to')[0].replace(' ','');
                var to = dateEntered.split('to')[1].replace(' ','');
                $http.get(from_to + 'from=' + from + '&to=' + to).success(
                    function(data, status)
                    {
                        console.log('Sucess');
                    }).error(function(error){ console.log("error")});
                var from_to_data = from_to + 'from=' + from + '&to=' + to
                console.log(from_to_data);
                $http({method:"GET", url:from_to_data}).success(function(result){
                    var final_data = result.result;
                    console.log(final_data);
                    self.high_data.push(final_data);
                    console.log(self.high_data[0].volumes_data.volume_values);
                    
                angular.extend(self.chartOptions5,{
                series: [{
                        name: 'Brands',
                        colorByPoint: true,
                        data: [{
                            name: 'DF',
                            y: self.high_data[0].error_count.DF
                        }, {
                            name: 'DD',
                            y: self.high_data[0].error_count.DD,
                            sliced: true,
                            selected: true
                        }, {
                            name: 'GC',
                            y: self.high_data[0].error_count.GC
                        }, {
                            name: 'FES',
                            y: self.high_data[0].error_count.FES
                        }, {
                            name: 'Compliance',
                            y: self.high_data[0].error_count.Compliance
                        }, {
                            name: 'LLP',
                            y: self.high_data[0].error_count.LLP
                        }, {
                            name: 'MD',
                            y: self.high_data[0].error_count.MD
                        }, {
                            name: 'Charges',
                            y: self.high_data[0].error_count.Charges
                        }, {
                            name: 'Legal',
                            y: self.high_data[0].error_count.Legal
                        }, {
                            name: 'CC',
                            y: self.high_data[0].error_count.CC
                        }]
                    }]  
             }); 

        angular.extend(self.chartOptions4.yAxis.title,{
                text: 'errors'
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
                            y: self.high_data[0].accuracy_graph.DF
                        }, {
                            name: 'DD',
                            y: self.high_data[0].accuracy_graph.DD,
                        }, {
                            name: 'GC',
                            y: self.high_data[0].accuracy_graph.GC
                        }, {
                            name: 'FES',
                            y: self.high_data[0].accuracy_graph.FES
                        }, {
                            name: 'Compliance',
                            y: self.high_data[0].accuracy_graph.Compliance
                        }, {
                            name: 'LLP',
                            y: self.high_data[0].accuracy_graph.LLP
                        }, {
                            name: 'MD',
                            y: self.high_data[0].accuracy_graph.MD
                        }, {
                            name: 'Charges',
                            y: self.high_data[0].accuracy_graph.Charges
                        }, {
                            name: 'Legal',
                            y: self.high_data[0].accuracy_graph.Legal
                        }, {
                            name: 'CC',
                            y: self.high_data[0].accuracy_graph.CC
                        }]

             }]
             });

           angular.extend(self.chartOptions, {
               chart: {
                 backgroundColor: "transparent"
               },
               xAxis: {
                 categories: self.high_data[0].data.date,
                 title: {
                  text: null
                 }
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
                                    console.log(self.names_2);
                                }).error(function(error){ console.log("error")});
                            //console.log(e.target.series.name);
                            //$("#hello").html(e.target.category);
                            //$("#temp").html(e.target.y);
                            $('#myModal').modal('show');
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

               credits: {
                enabled: false
               },

               series: [{
                name: 'DD',
                data: self.high_data[0].data.data.DD
                }, {
                name: 'DF',
                data: self.high_data[0].data.data.DF
                }, {
                name: 'CC',
                data: self.high_data[0].data.data.CC
                },{
                name: 'GC',
                data: self.high_data[0].data.data.GC
                },{
                name: 'Compliance',
                data: self.high_data[0].data.data.Compliance
                },{
                name: 'Legal',
                data: self.high_data[0].data.data.Legal
                },{
                name: 'MD',
                data: self.high_data[0].data.data.MD
                },{
                name: 'LLP',
                data: self.high_data[0].data.data.LLP
                },{
                name: 'Charges',
                data: self.high_data[0].data.data.Charges
                },{
                name: 'FES',
                data: self.high_data[0].data.data.FES
                }
                ]
             });

           angular.extend(self.chartOptions2, {
           chart : {
                 backgroundColor: "transparent",
                 type: 'bar'
               },
        title: {
            text: ''
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            categories: ["MD","LLP","CC","DD","Compliance","Legal","Charges","GC","FES"],
            //categories: ["DD"],
            title: {
                text: null
            }
        },
        yAxis: {
            gridLineColor: 'a2a2a2',
            min: 0,
            title: {
                text: 'total achieved',
                align: 'high'
            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            valueSuffix: ''
        },
       plotOptions: {
            series : {
                allowPointSelect: true,
                    point: {
                        events:{
                            select: function(e) {
                            console.log(e);
                            $("#wpp_hello").html(e.target.category);
                            $("#wpp_temp").html(e.target.y);
                            $('#workpacket_per').modal('show');
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
        /*legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -40,
            y: 80,
            floating: true,
            borderWidth: 1,
            backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
            shadow: true
        },*/
        credits: {
            enabled: false
        },
        series: [{
            name: 'Past Week',
            //data:[self.high_data[0].volumes_data.volume_values.DD]
            data:[self.high_data[0].volumes_data.volume_values.MD,
            self.high_data[0].volumes_data.volume_values.LLP,self.high_data[0].volumes_data.volume_values.CC,
            self.high_data[0].volumes_data.volume_values.DD,self.high_data[0].volumes_data.volume_values.Compliance,
            self.high_data[0].volumes_data.volume_values.Legal,self.high_data[0].volumes_data.volume_values.Charges,
            self.high_data[0].volumes_data.volume_values.GC,self.high_data[0].volumes_data.volume_values.FES]

        }]

             });

            angular.extend(self.chartOptions3,{
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
                text: ''
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

        series: [{
            colorByPoint: true,
            name: 'error count',
            data: self.high_data[0].volumes_data.volume_new_data,
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

                });

            }

            self.chartOptions = {};
            self.chartOptions2 = {};
            self.chartOptions3 = {};
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
                    text: 'errors'
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
            self.hideLoading();
            self.names;
            self.names_2;

            }],

            "bindings": {

              "hideLoading": "&",
              "showLoading": "&"
            }
         });

}(window.angular));
