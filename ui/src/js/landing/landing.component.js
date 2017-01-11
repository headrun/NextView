;(function (angular) {
  "use strict";

  angular.module("landing")
         .component("landing", {

           "templateUrl": "/js/landing/landing.html",
           "controller": ['$http','$scope','$rootScope',

           function ($http,$scope,$rootScope) {

             var self = this;

             $rootScope.sel_value = '';

             var project = 'api/project/';

             self.hideLoading();

             $('#Services').hide();

             $('#Widgets').hide();

             $('#Projects').hide();

             $('.mythili').hide();

             /*$(".pro_loading").click(function() {

                self.showLoading();

             });*/

              self.clickPro = function(val, $rootScope){

                self.showLoading();

                $('#dropdown_title').text(val.split(' - ')[1]);

                //self.cen_pro_name['state'] = val;

                //val = '';

                //self.updateState({'state':self.cen_pro_name, 'pageName':'page1'});

              }

            $("#Ser").click(function() {

                $("#About").hide();

                $("#Projects").hide();

                $("#Widgets").hide();

                $("#Services").show();
            });

            $("#Wid").click(function(){

                $("#Services").hide();

                $("#Widgets").show();

                $("#Projects").hide();

                $("#About").hide();
            });

            $("#Proj").click(function() {

                $("#Widgets").hide();

                $("#Services").hide();

                $("#About").hide();

                $("#Projects").show();

            });

            $("#Abt").click(function() {

                $("#About").show();

                $("#Services").hide();

                $("#Widgets").hide();

                $("#Projects").hide()

            });

            $("#Ser").on('click', function() {

                $("#Abt").removeClass('active');
            });

            $("#Wid").on('click', function() {

                $("#Abt").removeClass('active');
            });

            $("#Proj").on('click', function() {

                $("#Abt").removeClass('active');
            });



            $http({method:"GET", url:project}).success(function(result){

                self.pro_cen_nam = result.result.list[1];

                if (result.result.role == "customer") {

                    //var map_list = result.result.list;

                    //self.mapping_list = map_list[1];
                    //
                    self.mapping_list = [];
                    self.mapping_list.push(result.result.list[1]);

                }


                if (result.result.role == "team_lead") {

                    //var map_list = result.result.list;

                    //self.mapping_list = map_list[1];
                    self.mapping_list = []
                    self.mapping_list.push(result.result.list[1]);

                }

                if (result.result['role'] == "center_manager") {

                    var map_list = result.result.list;

                    self.mapping_list = map_list;

                    }

                if (result.result['role'] == "nextwealth_manager") {

                    var map_list = result.result.list;

                    self.mapping_list = map_list;

                    $('.mythili').show();

                    }
            });

         }],

            "bindings": {

              "hideLoading": "&",
              "showLoading": "&"
            }
         }); 
 
}(window.angular));
