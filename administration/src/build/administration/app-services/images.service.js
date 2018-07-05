(function () {
    'use strict';

    angular
        .module('administration')
        .service('imagesService', imagesService);

    imagesService.$inject = ['$http', '$log', '$window'];
    function imagesService($http, $log, $window) {
        var service = {
            isImage: isImage,
            isImageUrl: isImageUrl,
            readImageFile: readImageFile,
            getDefaultUserProfileImageUrl: getDefaultUserProfileImageUrl,
            getDefaultRoomPhotoUrl: getDefaultRoomPhotoUrl
        };

        return service;

        function isImage(file) {
            if ($window.FileReader) {
                return file.type.match('image.*') == true;
            }
        }

        function isImageUrl(url) {
            $http.get(url).then(function (response) {
                return true;
            }).catch(function (error) {
                $log.error('Log from images service: ', error);
                return false;
            });
        }

        function readImageFile(file, callback) {
            if ($window.FileReader) {
                var reader = new $window.FileReader();
                reader.onloadend = function (event) {
                    if (event.target.error === null) {
                        callback(reader.result);
                    }
                    else {
                        callback(null);
                    }
                };
                reader.readAsDataURL(file);
            }
        }

        function getDefaultUserProfileImageUrl() {
            return '/static/images/default.png';
        }

        function getDefaultRoomPhotoUrl() {
            return '/static/images/default-room.png';
        }
    }
})();