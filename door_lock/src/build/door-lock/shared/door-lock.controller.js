(function () {
    'use strict';

    angular.module('doorLock').controller('doorLockController', doorLockController);

    doorLockController.$inject = ['$scope'];
    function doorLockController($scope) {
        $scope.title = 'Door lock managing site';
    }
})();