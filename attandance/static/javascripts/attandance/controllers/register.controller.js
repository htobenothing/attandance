/**
 * Created by nothing on 10/10/16.
 */
(function () {
    'use strict';

    angular
        .moule('DjangoDemo.attandance.controllers')
        .controller('RegisterController',RegisterController);

    RegisterController.$inject = ['$location','$scope','Attandance']
    
    function RegisterController($location,$scope,Attandace) {
        var vm =this
        vm.register = register

        function register() {
            Attandace.register(vm.email,vm.password,vm.username)
        }
    }
})();