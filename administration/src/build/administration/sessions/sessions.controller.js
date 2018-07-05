(function () {
    'use strict';

    angular
        .module('administration')
        .controller('SessionsController', SessionsController);

    SessionsController.$inject = ['$log', 'sessionService'];
    function SessionsController($log, sessionService) {
        var self = this;
        var service = sessionService;

        self.list = [];
        self.orderOptions = [
            {id: 'id', name: 'ID sesije'},
            {id: 'key_id', name: 'ID ključa'},
            {id: 'user_id', name: 'ID korisnika'},
            {id: 'started_on', name: 'Datum preuzimanja'},
            {id: 'closed_on', name: 'Datum vraćanja'}
        ];
        self.orderProp = {id: 'started_on', name: 'Datum preuzimanja'};
        self.reverseOrder = true;

        self.selectAll = selectAll;
        self.deleteById = deleteById;
        self.deleteSelected = deleteSelected;

        init();

        function init() {
            service.sessions().then(function (response) {
                var data = response.data;
                var viewModel = [];
                for (var i = 0; i < data.length; i++) {
                    viewModel.push(JSON.parse(data[i]));
                }

                self.list = viewModel;
            });
        }

        function selectAll() {
            for (var i = 0; i < self.list.length; i++) {
                self.list[i].isSelected = !self.list[i].isSelected;
            }
        }

        function deleteById(id) {
            return service.sessionDelete(id).then(function (response) {
                return true;
            }).catch(function (error) {
                $log.error(' error: ' + error);
                return false;
            });
        }

        function deleteSelected() {
            var selectedList = self.list.filter(function (session) {
                return session.isSelected;
            });
            for (var i = 0; i < selectedList.length; i++) {
                if (!deleteById(selectedList[i].id)) {
                    $log.error('Failed to delete session with id ' + id.toString());
                }
            }
            self.list = self.list.filter(function (session) {
                return selectedList.indexOf(session) < 0;
            });
        }
    }
})();