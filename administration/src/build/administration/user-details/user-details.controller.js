(function () {
    'use strict';

    angular.module('administration').controller('UserDetailsController', UserDetailsController);

    UserDetailsController.$inject = ['$scope', '$routeParams', '$location', '$log', 'usersService'];
    function UserDetailsController($scope, $routeParams, $location, $log, usersService) {
        var service = usersService;

        $scope.model = {
            userId: $routeParams.id,
            userData: {}
        };
        $scope.deleteItem = deleteItem;

        init();

        function init() {
            service.getItem($scope.model.userId).then(function (response) {
                var data = response.data;
                $log.info('Raw data from response', data);
                $scope.model.userData = data;
            });
        }

        function deleteItem() {
            if ($scope.model.userData.isSelected) {
                service.userDelete($scope.model.userId).then(function (response) {
                    $location.url('/users');
                }).catch(function (error) {
                    window.alert(' error: ' + error);
                });
            }
        }
    }
})();