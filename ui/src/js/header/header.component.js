;(function (angular) {
  "use strict";

  angular.module("header")
         .component("header", {
           "templateUrl": "/js/header/header.html",
           "controller" : ["$rootScope", "$state", "$filter", "$interval","Session",

             function ($rootScope, $state, $filter, $interval , Session) {


               this.user = Session.get();
               console.log(this.user.roles);


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

                if((this.user.role == "Customer") || (this.user.role == "Team Lead") ){
                    $('#center_dropdown').hide();
                    $('#project_dropdown').hide();
                if (this.user.role == "Customer"){
                    $('#fileupload').hide();
                    }
                }
                if((this.user.role == "Nextwealth Manager") || (this.user.role == "Center Manager")){
                    $('#fileupload').hide();
                if (this.user.role == "Center Manager"){
                    $('#center_dropdown').hide();
                    }
                }

               var that = this;

               this.collapsed = false;

               this.toggleCollapse = function () {
               
               this.collapsed = !this.collapsed;
               }
             }
           ],
           "bindings": {
             "tabsOrder": "<",
             "tabs"     : "<",
             "activeTab": "<"
           }
         });
}(window.angular));
