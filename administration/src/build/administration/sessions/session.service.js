(function () {
    'use strict';

    angular
        .module('administration')
        .service('sessionService', SessionService);

    SessionService.$inject = ['$http'];
    function SessionService($http) {

        var service = {
            sessions: sessions,
            session: session,
            sessionDelete: sessionDelete
        };

        return service;

        function sessions() {
            return $http.get('/api/sessions');
        }

        function session(id) {
            return $http.get('/api/sessions/' + id.toString());
        }

        function sessionDelete(id) {
            return $http.delete('/api/sessions/delete/' + id.toString());
        }
    }
})();