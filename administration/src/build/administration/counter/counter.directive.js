(function () {
    'use-strict';

    angular
        .module('administration')
        .directive('counter', counter);

    counter.$inject = ['templateServiceProvider'];
    function counter(templateServiceProvider) {
        var appBaseUrl = templateServiceProvider.appBaseUrl();
        return {
            restrict: 'E',
            scope: {
                tagData: '='
            },
            controller: 'CounterController',
            templateUrl: appBaseUrl + '/counter/counter.html'
        };
    }
})();