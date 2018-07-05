(function () {
    'use strict';

    angular
        .module('administration')
        .service('searchSessionsService', searchSessionsService);

    searchSessionsService.$inject = ['$http'];
    function searchSessionsService($http) {
        var service = {
            getSessionsByKey:getSessionsByKey,
            getSessionsByUser: getSessionsByUser
        };

        return service;

        function getSessionsByKey(keyId) {
            return $http.get('/api/sessions/key/' + keyId.toString());
        }

        function getSessionsByUser(userId) {
            return $http.get('/api/sessions/user/' + userId.toString());
        }
    }
})();