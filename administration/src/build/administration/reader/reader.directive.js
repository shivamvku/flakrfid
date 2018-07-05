(function () {
    'use strict';

    angular
        .module('administration')
        .directive('reader', reader);

    reader.$inject = ['templateServiceProvider'];

    function reader(templateServiceProvider) {
        var appBaseUrl = templateServiceProvider.appBaseUrl();
        return {
            restrict: 'EA',
            scope: {
                // tagData: "=tagData",
                // message: "=message"
                tagData: "=",
                message: "="
            },
            templateUrl: appBaseUrl + '/reader/reader.html',
            controller: 'ReaderController'//,
            // controllerAs: 'rdc',
            // bindToController: true
        }
    }
})();