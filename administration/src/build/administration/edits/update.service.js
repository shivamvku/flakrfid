(function () {
    'use strict';
    angular.module('administration').service('updateService', updateService);

    updateService.$inject = ['$http', 'Upload'];
    function updateService($http, Upload) {
        var service = {
            getKey: getKey,
            getUser: getUser,
            updateKey: updateKey,
            updateUser: updateUser
        };

        return service;

        function getKey(keyId) {
            return $http.get('/api/key/get/' + keyId.toString());
        }

        function getUser(userId) {
            return $http.get('/api/user/get/' + userId.toString());
        }

        function updateKey(key) {
            return $http.put('/api/key/edit', JSON.stringify(key));
        }

        function updateUser(user, image) {
            return Upload.upload({
                url: '/api/user/edit',
                data: {file: image, 'user_json': JSON.stringify(user), 'user': user},
                method: 'PUT'
            }).then(function (response) {
                return response.status;
            }, function (error) {
                return error.status;
            })
        }
    }
})();