(function () {
    'use-strict';

    angular
        .module('administration')
        .controller('AuthDashboardController', AuthDashboardController);

    AuthDashboardController.$inject = ['$scope', '$location', 'authService', 'usersService'];
    function AuthDashboardController($scope, $location, authService, usersService) {
        $scope.logout = logout;
        $scope.editProfile = editProfile;

        $scope.$on('$routeChangeSuccess', function (event, newUrl, oldUrl) {
            init();
        });

        init();

        function init() {
            if (document.cookie.indexOf('token') > -1 && authService.isAuthenticated()) {
                var userCredentials = authService.getCredentials();
                if (userCredentials) {
                    if (userCredentials.hasOwnProperty('username')) {
                        var currentServiceUsername = userCredentials.username;
                        if ($scope.username != currentServiceUsername) {
                            setUsername(currentServiceUsername);
                        }
                    }
                }
            }
        }

        function setUsername(username) {
            setTimeout(function () {
                $scope.$apply(function () {
                    $scope.username = username;
                });
            }, 500);
        }

        function editProfile() {
            usersService.search($scope.username)
                .then(function (response) {
                    var userId = null;
                    angular.forEach(response.data, function (value, key) {
                        var user = JSON.parse(value);
                        if (user) {
                            userId = user.user_id;
                        }
                    });
                    if (userId) {
                        $location.url('/users/edit/' + userId.toString());
                    }
                });
        }

        function logout() {
            authService.clearCredentials();
            $location.path('/home');
        }
    }
})();