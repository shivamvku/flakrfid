(function () {
    'use strict';

    angular
        .module('administration')
        .controller('MainController', MainController);

    MainController.$inject = ['$scope'];
    function MainController($scope) {
        init();

        function init() {
            $scope.isAuthenticated = false;
        }
    }
})();