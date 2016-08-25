;(function (angular) {
  "use strict";

  angular.module("header")
         .component("header", {
           "templateUrl": "/js/header/header.html",
           "controller" : ["$rootScope", "$state", "$filter", "$interval","$http", "Session",

             function ($rootScope, $state, $filter, $interval , $http, Session) {

               var self = this;

               this.user = Session.get();

                if (this.user.roles.indexOf("team_lead") >= 0) {
                    this.user.role = "Team Lead";
                }
                if (this.user.roles.indexOf("customer") >= 0) {
                    this.user.role = "Customer";
                }
                if (this.user.roles.indexOf("center_manager") >= 0) {
                    this.user.role = "Center Manager";
                }
                if (this.user.roles.indexOf("nextwealth_manager") >= 0) {
                    this.user.role = "Nextwealth Manager";
                }
                if (this.user.role == "Customer") {
                    $('#fileupload').hide();
                }

               this.collapsed = false;

               this.toggleCollapse = function () {

               this.collapsed = !this.collapsed;
               }
              var project = 'api/project/';
              //self.projects_list = ['realshopee', 'dell', 'probe'];
              //self.centers_list = ['hubli', 'salem'];
              self.clickFun = function(val){
                console.log('Yesh clicked');
                //self.selectedValue = val;
                //var page = "page1";
                self.cen_pro_name['state'] = val;
                val = '';
                self.updateState({'state':self.cen_pro_name, 'pageName':'page1'});
                //self.updateState({'state':JSON.parse("{}"), 'pageName':'page1'});
                //self.cen_pro_name = {};
                //var resp_list = val.split(' - ');
                //console.log(resp_list);
                //self.cen_pro_name = val;
                //var page = "page1";
                //console.log(self.cen_pro_name);
                //var page = "page1";

                //self.selectDropdown({'state':self.cen_pro_name});

                //self.pro_name = resp_list[1];
                //self.project_name = self.center + ' - ' + val;
              }
              /*self.clickFun = function(val){
                self.project_name = self.center + ' - ' + val;
              }
              self.clickFun2 = function(val){
                self.project_name = val + ' - ' + self.ppp;
              }*/

                self.onChange = function(page) {
                    location.href = '#!'+page;
                   //$location.path('/'+page);
                }


              $http({method:"GET", url:project}).success(function(result){

                //console.log('from project api');
                //console.log(result.result.list[0]);

                if (result.result.role == "customer") {
                    if (result.result.list[0] == "none") {
                        $('#select_dropdown').hide();
                    }
                    var map_list = result.result.list;
                    self.mapping_list = map_list;
                }


                /*if (result.result['role'] == "center_manager")
                    {
                    var center = result.result['center'];
                    self.center = center;
                    var proj_list = result.result['project'];
                    self.proj_list = proj_list;
                    self.project_name = center + ' - ' + proj_list[0];
                    }
                else if (result.result['role'] == "nextwealth_manager"){
                    self.centers = result.result.cen_pro;
                    console.log(self.centers);
                    //var keys = Object.keys(result.result);
                    //var cent_list = [];
                    //var prj_list = [];
                    cent_list.push(keys[0]);
                    cent_list.push(keys[2]);
                    var one = result.result[keys[0]];
                    for (var i=0; i < one.length; i++){
                        prj_list.push(one[i])
                    }
                    var two = result.result[keys[2]];
                    for (var j=0; j < two.length; j++){
                        prj_list.push(two[j])
                    }
                    self.proj_list = prj_list;
                    self.centers_list = cent_list;
                    //prj_list.push(result.result[keys[2]])
                    //for (i=0; i < keys.length; i++){
                    //}
                    //console.log(keys[2]);
                    self.project_name = cent_list[0] + ' - ' + prj_list[0];
                    self.center = cent_list[0];
                    self.ppp = prj_list[0];


                }
                else if (result.result['role'] == "customer"){
                    console.log('Customer logged in');
                }
                else {
                    self.project_name = result.result;
                    }*/
                //console.log(self.project_name);
              });
              self.project_name = '';
              self.proj_list = '';
              self.center = '';
              self.ppp = '';
              self.mapping_list = '';
              self.center_list = [];
              self.cen_pro_name = {};
              //self.pro_name = '';
             }
           ],
           "bindings": {
             "tabsOrder"  : "<",
             "tabs"       : "<",
             "activeTab"  : "<",
             "updateState": "&",
             "selectedValue": "=",
             "selectDropdown": "&"
           }
         });
}(window.angular));
