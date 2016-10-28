/**
 * Created by nothing on 10/10/16.
 */
(function () {
    'use strict';
    angular
        .module('djangoDemo.config')
        .config(config)

    function config($locationProvider) {
        $locationProvider.html5Mode(true);
        $locationProvider.hashPrefix('#!');
    }
})