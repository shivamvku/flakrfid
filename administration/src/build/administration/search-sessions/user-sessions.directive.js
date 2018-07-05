(function () {
    'use strict';

    angular
        .module('administration')
        .directive('userSessions', userSessions);

    userSessions.$inject = ['templateServiceProvider'];
    function userSessions(templateServiceProvider) {
        var appBaseUrl = templateServiceProvider.appBaseUrl();
        return {
            restrict: 'EA',
            scope: {
                userId: '='
            },
            templateUrl: appBaseUrl + '/search-sessions/user-sessions.html',
            controller: 'UserSessionsController'
        };
    }
})();