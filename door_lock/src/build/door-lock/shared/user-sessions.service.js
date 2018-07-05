(function () {
    'use strict';

    angular.module('doorLock').service('userSessionsService', userSessionsService);

    userSessionsService.$inject = ['$http'];
    function userSessionsService($http) {
        var service = {
            getItems: getItems
        };

        return service;

        function getItems() {
            return $http.get('');
        }
    }
})();