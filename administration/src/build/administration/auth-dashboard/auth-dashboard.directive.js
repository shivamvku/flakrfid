(function () {
    'use-strict';

    angular
        .module('administration')
        .directive('authDashboard', authDashboard);

    authDashboard.$inject = ['templateServiceProvider'];
    function authDashboard(templateServiceProvider) {
        var appBaseUrl = templateServiceProvider.appBaseUrl();
        return {
            restrict: 'EA',
            scope: false,
            controller: 'AuthDashboardController',
            templateUrl: appBaseUrl + '/auth-dashboard/auth-dashboard.html'
        }
    }
})();