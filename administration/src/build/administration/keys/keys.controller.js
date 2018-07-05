(function () {
    'use strict';
    angular.module('administration').controller('KeysController', KeysController);

    KeysController.$inject = ['$location', '$log', 'keysService'];
    function KeysController($location, $log, keysService) {
        var self = this;
        var service = keysService;

        self.deleteSelected = deleteSelected;
        self.toImport = toImport;
        self.orderOptions = [
            {id: 'id', name: 'ID ključa'},
            {id: 'tag_id', name: 'Tag ID ključa'},
            {id: 'room_id', name: 'Broju prostorije'},
            {id: 'sector_name', name: 'Odjelu'},
            {id: 'room_repr', name: 'Punom zapisu'}
        ];

        init();

        function init() {
            service.getItems().then(function (response) {
                var data = response.data;
                var viewModel = [];
                for (var i = 0; i < data.length; i++) {
                    var singleViewModel = data[i];
                    viewModel.push(JSON.parse(singleViewModel));
                }
                self.list = viewModel;
            });
        }

        function deleteById(id) {
            return service.keyDelete(id).then(function (response) {
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

        function toImport() {
            $location.url('/keys/seed');
        }
    }
})();