(function () {
    'use strict';
    angular.module('administration').controller('UserEditController', UserEditController);

    UserEditController.$inject = ['$scope', '$log', '$routeParams', '$location', 'updateService'];
    function UserEditController($scope, $log, $routeParams, $location, updateService) {
        var userId = $routeParams.id;
        var service = updateService;

        $scope.title = "Stranica za uređivanje podataka korisnika";
        $scope.note = "Uredite podatke korisnika pridruživanjem informacija o RFID kartici sa podacima o korisniku";

        $scope.tagInfo = {
            tagId: "",
            message: ""
        };
        $scope.isPreloading = true;
        $scope.roleOptions = [
            {id: 1, name: 'Profesor'},
            {id: 2, name: 'Student'}
        ];

        $scope.proceed = proceed;
        $scope.cancel = cancel;
        $scope.isNotValid = isNotValid;

        init();

        function init() {
            service.getUser(userId).then(function (response) {
                var user = response.data;
                $log.info('User info loaded: ', user);
                $scope.tagInfo.tagId = user.tag_id;
                $scope.email = user.email;
                $scope.firstName = user.first_name;
                $scope.lastName = user.last_name;
                $scope.role = $scope.roleOptions.filter(function (roleOpt) {
                    return roleOpt.id == user.role_id;
                })[0].id;
                $scope.image = user.pic_url;
            }).catch(function (error) {
                $log.error('Failed to load user data... ' + error.data);
                $location.url('/home');
            });
        }

        function isNotValid() {
            return ($scope.tagInfo.tagId == '' || $scope.firstName == '' || $scope.lastName == '' || $scope.email == '' || $scope.role == '');
        }

        function proceed() {
            var user = {
                id: userId,
                tag_id: $scope.tagInfo.tagId,
                first_name: $scope.firstName,
                last_name: $scope.lastName,
                email: $scope.email,
                role_id: $scope.role
            };
            $log.info('User data is ', user);
            var image = $scope.image;
            $log.info('Image name is ', image);
            service.updateUser(user, image).then(function (status) {
                if (status == 200) {
                    $location.url('/users');
                }
                else {
                    $log.error('Error status: ', status);
                }
            }).catch(function (error) {
                $log.error('Error status: ', error);
            });
        }

        function cancel() {
            $location.url('/home');
        }
    }
})();