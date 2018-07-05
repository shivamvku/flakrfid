(function () {
    'use strict';
    angular.module('doorLock').config(config);

    config.$inject = ['$routeProvider', '$locationProvider'];
    function config($routeProvider, $locationProvider) {

        var appBaseUrl = angular.element(document.querySelector('base')).attr('href') + 'static/door-lock';

        $locationProvider.html5Mode({
            enabled: true,
            requireBase: false,
            rewriteLinks: true
        });

        $routeProvider.when('/', {
            templateUrl: appBaseUrl + '/home/home.html',
            controller: 'HomeController',
            controllerAs: 'home'
        }).otherwise({redirectTo: '/home'});
    }
})();