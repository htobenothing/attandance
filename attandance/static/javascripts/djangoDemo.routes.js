/**
 * Created by nothing on 10/10/16.
 */
(function () {
    'use strict';
    angular
        .module('django.routes')
        .config(config)

    config.$inject = ['$routerProvider'];

    function config($routeProvider) {
        $routeProvider.caseInsensitive = true
        $routeProvider
            .when('/register', {
                controller: 'RegisterController',
                controllerAs: 'vm',
                templateUrl: '/static/templates/attandance/register.html'
            })
            .when('/login',{
                
            })
            .otherwise('/')
    }
})