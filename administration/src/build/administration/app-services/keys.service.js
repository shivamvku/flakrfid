(function () {
    'use strict';

    angular
        .module('administration')
        .service('keysService', keysService);

    keysService.$inject = ['$http'];
    function keysService($http) {
        var service = {
            search: search,
            getItems: getItems,
            getItem: getItem,
            keyDelete: keyDelete
        };

        return service;

        function search(roomId) {
            return $http.get('/api/keys/search/' + roomId.toString());
        }

        function getItems() {
            return $http.get('api/keys');
        }

        function getItem(keyId) {
            return $http.get('/api/key/get/' + keyId.toString());
        }

        function keyDelete(id) {
            return $http.delete('/api/key/delete/' + id.toString());
        }
    }
})();