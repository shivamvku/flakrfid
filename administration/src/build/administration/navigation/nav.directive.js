(function () {
    'use strict';

    angular
        .module('administration')
        .directive('navBar', navBar);

    navBar.$inject = ['templateServiceProvider'];
    function navBar(templateServiceProvider) {
        var appBaseUrl = templateServiceProvider.appBaseUrl();
        return {
            restrict: 'E',
            scope: false,
            templateUrl: appBaseUrl + '/navigation/navigation.html',
            controller: 'NavController'
        };
    }
})();