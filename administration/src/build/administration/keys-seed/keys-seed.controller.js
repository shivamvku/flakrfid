(function () {
    'use strict';

    angular.module('administration').controller('KeysSeedController', KeysSeedController);

    KeysSeedController.$inject = ['$http', '$location', '$window', '$log', 'Upload'];
    function KeysSeedController($http, $location, $window, $log, Upload) {

        var self = this;

        self.getTemplate = getTemplate;
        self.send = send;
        self.cancel = cancel;

        function getTemplate() {
            $http.get('/api/data/template').then(function (response) {
                var data = response['file'];
                $log.info('Filename is ', data);
                $window.open('/api/data/template');
            });
        }

        function send() {
            Upload.upload({
                url: '/api/data/import',
                data: {file: self.file}
            }).then(function (response) {
                $log.info('Success ', response);
                $location.url('/keys');
            }, function (error) {
                $log.error('Error status: ', error);
            });
        }

        function cancel() {
            $location.url('/home');
        }
    }
})();