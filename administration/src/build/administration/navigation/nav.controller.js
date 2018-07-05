(function () {
    'use strict';

    angular
        .module('administration')
        .controller('NavController', NavController);

    NavController.$inject = ['$scope', '$location', 'authService'];
    function NavController($scope, $location, authService) {
        $scope.isAuthenticated = false;
        $scope.setActive = setActive;
        $scope.isActive = isActive;

        $scope.title = 'RFID sustav';
        $scope.commonRoutes = [
            {id: 0, route: '/', name: 'Naslovnica'}
        ];
        $scope.protectedRoutes = [
            {id: 1, route: '/sessions', name: 'Preuzimanja ključeva'},
            {id: 2, route: '/keys/search', name: 'Pretraga ključeva'},
            {id: 3, route: '/keys/seed', name: 'Uvoz ključeva'},
            {id: 4, route: '/keys/register', name: 'Registracija ključa'},
            {id: 5, route: '/keys', name: 'Prostorije'},
            {id: 6, route: '/users', name: 'Korisnici'},
            {id: 7, route: '/users/search', name: 'Pretraga korisnika'}
        ];
        $scope.authenticationRoutes = [
            {id: 8, route: '/login', name: 'Prijava korisnika'},
            {id: 9, route: '/users/register', name: 'Registracija korisnika'}
        ];

        $scope.$on('$routeChangeStart', function (event, newUrl, oldUrl) {
            if (newUrl.$$route != undefined) {
                var originalPath = newUrl.$$route.originalPath;
                var _guestRoutes = guestRoutes();
                var doReturn = false;
                angular.forEach(_guestRoutes, function (value, key) {
                    if (value == originalPath) {
                        doReturn = true;
                    }
                });

                console.log('From naviagation ', $scope.isAuthenticated);
                if (authService.getCredentials != undefined) {
                    $scope.isAuthenticated = !!authService.getCredentials();
                }
                else {
                    $scope.isAuthenticated = false;
                }

                if (!doReturn) {
                    if (!$scope.isAuthenticated) {
                        event.preventDefault();
                        $location.url('/login');
                    }
                }
            }
        });

        $scope.$on('$routeChangeSuccess', function (event, newUrl, oldUrl) {
            if (authService.getCredentials != undefined) {
                $scope.isAuthenticated = authService.isAuthenticated();
                if ($scope.isAuthenticated) {
                    var globals = authService.getCredentials();
                    authService.setCredentials(globals.username, globals.token);
                }
            }
            if (newUrl.$$route != undefined) {
                var originalPath = newUrl.$$route.originalPath.substring(1);
                checkPath(originalPath);
            }
        });

        function setActive(tabId) {
            $scope.tab = tabId;
        }

        function isActive(tabId) {
            return $scope.tab === tabId;
        }

        function checkPath(originalPath) {
            var availableRoutes = $scope.commonRoutes.concat($scope.protectedRoutes);
            if (!$scope.isAuthenticated) {
                availableRoutes = availableRoutes.concat($scope.authenticationRoutes);
            }
            for (var i = 0; i < availableRoutes.length; i++) {
                if (availableRoutes[i].route == originalPath) {
                    setActive(availableRoutes[i].id);
                    return true;
                }
            }
            return false;
        }

        function guestRoutes() {
            return [
                '/home',
                '/login',
                '/users/register'
            ]
        }
    }
})();