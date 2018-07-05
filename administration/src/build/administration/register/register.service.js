(function () {
    'use strict';

    angular
        .module('administration')
        .service('registerService', registerService);

    registerService.$inject = ['$http', 'Upload'];
    function registerService($http, Upload) {
        var service = {
            userId: userId,
            keyId: keyId,
            registerKey: registerKey,
            registerUser: registerUser
        };

        return service;

        function registerKey(key) {
            return $http.post('/api/keys/register', JSON.stringify(key));
        }

        // function registerUser(user) {
        function registerUser(user, image) {
            return Upload.upload({
                url: '/api/users/register',
                data: {file: image, 'user_json': JSON.stringify(user), 'user': user},
                method: 'POST'
            });
            // return $http.post('/api/users/register', JSON.stringify(user));
        }

        function userId(tagData) {
            return $http.get('/api/users/tag/search/' + tagData);
        }   // returns user ID

        function keyId(tagData) {
            return $http.get('/api/keys/tag/search/' + tagData);
        }   // returns key ID
    }
})();