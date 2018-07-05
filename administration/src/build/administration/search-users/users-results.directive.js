(function () {
    'use strict';
    angular
        .module('administration')
        .directive('usersSearchResults', usersSearchResults);

    usersSearchResults.$inject = ['templateServiceProvider'];
    function usersSearchResults(templateServiceProvider) {
        var appBaseUrl = templateServiceProvider.appBaseUrl();
        return {
            restrict: 'EA',
            scope: {
                results: '='
            },
            templateUrl: appBaseUrl+ '/search-users/users-results.html'
        };
    }
})();