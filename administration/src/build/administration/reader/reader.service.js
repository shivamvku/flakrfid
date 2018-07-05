(function () {
    'use strict';

    angular
        .module('administration')
        .service('readerService', readerService);

    readerService.$inject = ['$http'];
    function readerService($http) {
        var service = {
            initReader: initReader
        };

        return service;

        function initReader() {
            return $http.get('/api/reader');
        }
    }
})();