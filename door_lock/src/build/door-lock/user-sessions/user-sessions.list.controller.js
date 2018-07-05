(function () {
    'use strict';

    angular.module('doorLock').controller('UserSessionsListController', serSessionsListController);

    UserSessionsListController.$inject = ['$log', 'userSessionsService'];
    function UserSessionsListController($log, userSessionsService) {
        var service = userSessionsService;
        var self = this;
        self.userSessions = [];

        activate();

        function activate() {
            service.getItems().then(function (response) {
                $log.info('Retrieved user sessions from server', response.data.data);
                self.userSessions = response.data.data;
            }).catch(function (error) {
                $log.error('Error on retrieving from the server: ', error);
            });
        }
    }
})();