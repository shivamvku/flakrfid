(function () {
    'use strict';

    angular
        .module('administration')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['$scope'];
    function HomeController($scope) {
        $scope.title = "Sustav za upravljanje i organizaciju ključeva od prostorija temeljen na RFID tehnologiji";
        $scope.message = 'Web aplikacija za upravljanje, preuzimanje i vraćanje preuzetih ključeva prostorija.';
    }
})();
