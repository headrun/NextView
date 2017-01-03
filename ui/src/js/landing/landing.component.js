;(function (angular) {
  "use strict";

  angular.module("landing")
         .component("landing", {

           "templateUrl": "/js/landing/landing.html",
           "controller": ['$http',

           function ($http) {

             var self = this;

             self.hideLoading();

            }],

            "bindings": {

              "hideLoading": "&",
              "showLoading": "&"
            }
         });

}(window.angular));
