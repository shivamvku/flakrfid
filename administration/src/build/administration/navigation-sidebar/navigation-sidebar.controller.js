(function () {
    'use-strict';

    angular
        .module('administration')
        .controller('SidebarController', SidebarController);

    SidebarController.$inject = ['$scope'];
    function SidebarController($scope) {
        $scope.basic = {label: 'Opcije brze pretrage'};
        $scope.extended = {label: 'Pregled svih podataka'};
        $scope.settings = {label: 'Opcije za pohranu'};

        $scope.slideSidebar = slideSidebar;

        $scope.basicRoutes = [
            {id: 7, route: '/users/search', name: 'Pretraga korisnika'},
            {id: 2, route: '/keys/search', name: 'Pretraga ključeva'}
        ];
        $scope.extendedRoutes = [
            {id: 1, route: '/sessions', name: 'Preuzimanja ključeva'},
            {id: 6, route: '/users', name: 'Korisnici'},
            {id: 5, route: '/keys', name: 'Prostorije'}
        ];
        $scope.settingsRoutes = [
            {id: 4, route: '/keys/register', name: 'Registracija ključa'},
            {id: 3, route: '/keys/seed', name: 'Uvoz ključeva'}
        ];

        function slideSidebar() {
            $scope.showSide = !$scope.showSide;
        }
    }
})();