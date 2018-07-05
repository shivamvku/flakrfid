(function () {
    'use strict';

    angular
        .module('administration')
        .controller('UsersController', UsersController);

    UsersController.$inject = ['$log', 'usersService', 'imagesService'];
    function UsersController($log, usersService, imagesService) {
        var self = this;
        var service = usersService;
        var images = imagesService;

        self.orderOptions = [
            {id: 'user_id', name: 'ID korisnika'},
            {id: 'tag_id', name: 'Tag ID'},
            {id: 'role_id', name: 'Titula'},
            {id: 'first_name', name: 'Ime'},
            {id: 'last_name', name: 'Prezime'},
            {id: 'email', name: 'Email'}
        ];

        self.deleteSelected = deleteSelected;

        init();

        function init() {
            service.getItems().then(function (response) {
                console.log('Response data: ', response.data);
                var data = response.data;
                var viewModel = [];
                angular.forEach(data, function (value, key) {
                    var singleViewModel = JSON.parse(value);
                    if ("" === singleViewModel.pic_url) {
                        singleViewModel.pic_url = images.getDefaultUserProfileImageUrl();
                    }
                    this.push(singleViewModel)
                }, viewModel);
                self.list = viewModel;
            }).catch(function (error) {
                console.log('Error loading users: ', error);
            })
        }

        function deleteById(id) {
            return service.userDelete(id).then(function (response) {
                return true;
            }).catch(function (error) {
                $log.error(' error: ' + error);
                return false;
            });
        }

        function deleteSelected() {
            var selectedList = self.list.filter(function (user) {
                return user.isSelected;
            });
            $log.info('Selected users: ', selectedList);
            for (var i = 0; i < selectedList.length; i++) {
                if (!deleteById(selectedList[i].user_id)) {
                    $log.error('Failed to delete session with id ' + selectedList[i].user_id.toString());
                }
            }
            self.list = self.list.filter(function (session) {
                return selectedList.indexOf(session) < 0;
            });
        }
    }
})();