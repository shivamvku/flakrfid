(function () {
    'use strict';

    angular
        .module('administration')
        .controller('KeyRegisterController', KeyRegisterController);

    KeyRegisterController.$inject = ['$scope', '$log', '$location', 'registerService'];
    function KeyRegisterController($scope, $log, $location, registerService) {
        var service = registerService;

        $scope.title = "Stranica za registraciju ključeva";
        $scope.note = "Registrirajte ključ i prostoriju pridjeljujući broj prostorije s ostalim podacima poput odjela.";

        $scope.tagInfo = {
            tagId: "",
            message: ""
        };
        $scope.isRoom = 1;

        $scope.proceed = proceed;
        $scope.cancel = cancel;

        function proceed() {
            $log.info('Tag ID: ', $scope.tagInfo.tagId);
            var key = {
                id: -1,
                tag_id: $scope.tagInfo.tagId,
                room_id: $scope.roomId,
                block_name: $scope.blockName,
                sector_name: $scope.sectorName,
                floor: $scope.floor
            };
            $log.info('Key: ', key);
            service.registerKey(key)
                .then(function (response) {
                    if (response.status == 200) {
                        $location.url('/home');
                    }
                    else {
                        $log.debug('Response status is not 200 on registering key: ' + response.data);
                    }
                })
                .catch(function (error) {
                    $log.error('Failed to create key... ' + error.data);
                });
        }

        function cancel() {
            $location.url('/home');
        }
    }
})();