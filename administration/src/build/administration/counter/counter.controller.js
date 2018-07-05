(function () {
    'use-strict';

    angular
        .module('administration')
        .controller('CounterController', CounterController);

    CounterController.$inject = ['$scope', '$timeout'];
    function CounterController($scope, $timeout) {
        $scope.message = ' OPREZ! Vremena preostalo za očitanje: ';
        $scope.counter = 60;

        var updateCounter = function () {
            $scope.counter--;
            if ($scope.counter >= 0 && $scope.tagData == '') {
                $timeout(updateCounter, 1000);
            }
            else {
                $scope.counter = 0;
            }
        };

        updateCounter();
    }
})();