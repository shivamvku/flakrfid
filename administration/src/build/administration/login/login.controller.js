(function () {
    'use-strict';

    angular
        .module('administration')
        .controller('LoginController', LoginController);

    LoginController.$inject = ['$scope', '$log', '$location', 'authService'];
    function LoginController($scope, $log, $location, authService) {
        $scope.loginErrror = {};

        $scope.doLogin = doLogin;
        $scope.isValid = isValid;

        function isValid() {
            var _isValid = true;
            $scope.loginError = {};

            if (!$scope.email) {
                $scope.loginError.email = 'Ovo polje je obavezno!';
                _isValid = false;
            }
            if (!$scope.password) {
                $scope.loginError.password = 'Ovo polje je obavezno!';
                _isValid = false;
            }
            if ($scope.password && $scope.password.length < 9) {
                $scope.loginError.password = 'Lozinka je sigurna kao ima više od 8 znakova!';
                _isValid = false;
            }
            return _isValid;
        }

        function doLogin() {
            if (isValid()) {
                $log.info('Entered the login controller...');
                authService.login($scope.email, $scope.password)
                    .then(function (response) {
                        $log.debug('Login response data: ', response.data);
                        var token = response.data;
                        var globals = authService.setCredentials($scope.email, token);
                        if (globals) {
                            $log.debug('Auth data after login: ', globals);
                            $location.url('/home');
                        }
                    })
                    .catch(function (error) {
                        $log.error(error);
                        $scope.loginError.non_field_error = error.data.message;
                    });
            }
        }
    }
})();