(function () {
    'use-strict';

    angular
        .module('administration')
        .service('authService', authService);

    authService.$inject = ['$http', '$cookies'];
    function authService($http, $cookies) {
        var service = {
            login: login,
            setCredentials: setCredentials,
            clearCredentials: clearCredentials,
            getCredentials: getCredentials,
            isAuthenticated: isAuthenticated
        };

        return service;

        function login(email, password) {
            var authData = {email: email, password: password};
            return $http.post('/api/login', JSON.stringify(authData));
        }

        function setCredentials(username, token) {
            var globals = {
                username: username,
                token: token
            };
            $cookies.putObject('token', globals);

            $http.defaults.headers.common['Authorization'] = 'Token ' + token;
            return getCredentials();
        }

        function clearCredentials() {
            $cookies.remove('token');
            $http.defaults.headers.common['Authorization'] = 'Token ';
        }

        function getCredentials() {
            return $cookies.getObject('token')
        }

        function isAuthenticated() {
            return !!$cookies.getObject('token')
        }
    }
})();