/**
 * Created by nothing on 10/10/16.
 */
(function () {
    'use strict';
    angular
        .module('djangoDemo.attandance',[
            'dajngoDemo.attandance.controllers',
            'dajngoDemo.attandance.services'
        ]);

    angular
        .module('djangoDemo.attandance.controllers',[]);

    angular
        .module('djangoDemo.attandance.services',['ngCookies']);
})