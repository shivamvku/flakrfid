(function () {
    'use strict';

    angular.module('administration').controller('KeyDetailsController', KeyDetailsController);

    KeyDetailsController.$inject = ['$scope', '$routeParams', '$location', '$log', 'keysService'];
    function KeyDetailsController($scope, $routeParams, $location, $log, keysService) {
        var service = keysService;

        $scope.model = {
            keyId: $routeParams.id,
            keyData: {}
        };
        $scope.deleteItem = deleteItem;

        init();

        function init() {
            service.getItem($scope.model.keyId).then(function (response) {
                var data = response.data;
                $log.info('Raw data from response is: ', data);
                $scope.model.keyData = data;
            });
        }

        function deleteItem() {
            if ($scope.model.userData.isSelected) {
                service.keyDelete($scope.model.keyId).then(function (response) {
                    $location.url('/keys');
                }).catch(function (error) {
                    window.alert(' error: ' + error);
                });
            }
        }
    }
})();