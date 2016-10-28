/**
 * Created by nothing on 10/10/16.
 */
(function () {
    'use strict';

    angular.module('djangoDemo', [
        'djangoDemo.routes',
        'djangoDemo.attandance',
        'djangoDemo.config'
    ]);

    angular.module('djangoDemo.routes', ['ngRoute']);

    angular.module('djangoDemo.config', []);

    angular.module('djangoDemo').run(run);

    run.$inject = ['$http'];
    function run($http) {
        $http.defaults.xsrfHeadName = 'X-CSRFToken';
        $http.defaults.xsrfCookieName = 'csrftoken';
    }
})