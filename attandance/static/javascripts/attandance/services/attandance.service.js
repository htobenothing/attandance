/**
 * Created by nothing on 10/10/16.
 */
(function () {

    'use strict';
    angular
        .moule('DjangoDemo.attandance.services')
        .factory('Attandance', Attandance)

    Attandance.$inject = ['$cookies', '$http']

    function Attandance($cookies, $http) {

        var Attandance = {
            register: register
        };
        return Attandance;
    }

    function register(email, password, username) {
        return $http.post('/api/v1/accounts/', {
            username: username,
            password: password,
            email: email
        });
    }


})();