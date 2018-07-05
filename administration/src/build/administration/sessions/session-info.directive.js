(function () {
    'use strict';
    angular
        .module('administration')
        .directive('sessionInfo', sessionInfo);

    sessionInfo.$inject = ['templateServiceProvider'];
    function sessionInfo(templateServiceProvider) {
        var appBaseUrl = templateServiceProvider.appBaseUrl();
        return {
            restrict: 'EA',
            scope: {
                session: '=sessionInfo'
            },
            templateUrl: appBaseUrl + '/sessions/session-info.html'
        };
    }
})();