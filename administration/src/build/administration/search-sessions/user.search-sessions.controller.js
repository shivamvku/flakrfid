(function () {
    'use strict';

    angular
        .module('administration')
        .controller('UserSessionsController', UserSessionsController);

    UserSessionsController.$inject = ['$scope', '$timeout', 'searchSessionsService'];
    function UserSessionsController($scope, $timeout, searchSessionsService) {
        var service = searchSessionsService;

        $scope.orderOptions = [
            {id: 'id', name: 'ID sesije'},
            {id: 'key_id', name: 'ID ključa'},
            {id: 'user_id', name: 'ID korisnika'},
            {id: 'started_on', name: 'Datum preuzimanja'},
            {id: 'closed_on', name: 'Datum vraćanja'}
        ];

        init();

        function init() {
            service.getSessionsByUser($scope.userId).then(function (response) {
                $timeout(function () {
                    $scope.$apply(function () {
                        var data = response.data;
                        var viewModel = [];
                        for (var i = 0; i < data.length; i++) {
                            viewModel.push(JSON.parse(data[i]));
                        }
                        $scope.result = viewModel;
                    });
                }, 0);
            });
        }
    }
})();