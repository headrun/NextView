;(function (angular) {
  "use strict";

  angular.module("header")
         .component("header", {
           "templateUrl": "/js/header/header.html",
           "controller" : ["$rootScope", "$state", "$filter", "$interval","Session",

             function ($rootScope, $state, $filter, $interval , Session) {


               this.user = Session.get();
               console.log(this.user.roles);


                if (this.user.roles.indexOf("Agent") >= 0) {
                this.user.role = "Agent";
                }

                if (this.user.roles.indexOf("customer") >= 0) {
                this.user.role = "Customer";
                }
                if (this.user.roles.indexOf("Center_Manager") >= 0) {
                this.user.role = "Center Manager";
                }
                if (this.user.roles.indexOf("Nextwealth_Manager") >= 0) {
                this.user.role = "Nextwealth Manager";
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
