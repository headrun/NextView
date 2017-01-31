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

             $('#About').hide();

             //$('#Projects').hide();

             $('.mythili').hide();


              self.clickPro = function(val, $rootScope){

                self.showLoading();

                $('#dropdown_title').text(val.split(' - ')[1]);

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

                $("#Proj").removeClass('active');
            });

            $("#Wid").on('click', function() {

                $("#Proj").removeClass('active');
            });

            $("#Abt").on('click', function() {

                $("#Proj").removeClass('active');
            });



            $http({method:"GET", url:project}).success(function(result){

                self.pro_cen_nam = result.result.list[1];

                if (result.result.role == "customer") {

                    self.mapping_list = [];
                    self.mapping_list.push(result.result.list[1]);

                }


                if (result.result.role == "team_lead") {

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
