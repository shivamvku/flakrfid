(function () {
    'use strict';
    angular.module('administration').controller('KeyEditController', KeyEditController);

    KeyEditController.$inject = ['$scope', '$log', '$routeParams', '$location', 'updateService'];
    function KeyEditController($scope, $log, $routeParams, $location, updateService) {
        var keyId = $routeParams.id;
        var service = updateService;

        $scope.title = "Stranica za uređivanje podataka o ključu";
        $scope.note = "Uredite podatke o ključu i prostoriji pridjeljujući broj prostorije s ostalim podacima poput odjela.";

        $scope.tagInfo = {
            tagId: "",
            message: ""
        };
        $scope.isRoom = 1;
        $scope.isPreloading = true;

        $scope.proceed = proceed;
        $scope.cancel = cancel;

        $scope.$watch('tagInfo.tagId', function (previous, updated) {
            $log.info('Previous tag data: ', previous);
            $log.info('New tag data: ', updated);
        });

        init();

        function init() {
            service.getKey(keyId).then(function (response) {
                var key = response.data;
                $log.info('Key info loaded: ', key);
                $scope.isRoom = (key.block_name.includes('F') && key.sector_name.includes('A')) ? 2 : 1;
                $scope.tagInfo.tagId = key.tag_id;
                $scope.roomId = key.room_id;
                $scope.blockName = key.block_name;
                $scope.sectorName = key.sector_name;
                $scope.floor = key.floor;
                $scope.roomRepr = key.room_repr;
                $scope.isPreloading = false;
                $log.info('TagID: ', $scope.tagInfo.tagId);
            }).catch(function (error) {
                $log.error('Failed to load key data... ' + error.data);
                $location.url('/home');
            });
        }

        function proceed() {
            $log.info('TagID: ', $scope.tagInfo.tagId);
            var key = {
                id: keyId,
                tag_id: $scope.tagInfo.tagId,
                room_id: $scope.roomId,
                block_name: $scope.blockName,
                sector_name: $scope.sectorName,
                floor: $scope.floor,
                room_repr: $scope.roomRepr
            };
            $log.info('Key: ', key);
            service.updateKey(key).then(function (response) {
                $log.info('Updated key: ' + response.data);
                $location.url('/keys');
            }).catch(function (error) {
                $log.error('Failed to create key... ' + error.data);
            });
        }

        function cancel() {
            $location.url('/home');
        }
    }
})();