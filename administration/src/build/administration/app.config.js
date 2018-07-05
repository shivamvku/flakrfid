(function () {
    'use strict';

    angular
        .module('administration')
        .config(config);

    config.$inject = ['$routeProvider', '$locationProvider', '$httpProvider'];

    function config($routeProvider, $locationProvider) {
        var appBaseUrl = angular.element(document.querySelector('base')).attr('href') +
            'static/html';

        $locationProvider.html5Mode({
            enabled: true,
            requireBase: false,
            rewriteLinks: true
        });

        $routeProvider.when('/home', {
            templateUrl: appBaseUrl + '/home/home.html',
            controller: 'HomeController',
            controllerAs: 'home'
        }).when('/login', {
            templateUrl: appBaseUrl + '/login/login.html',
            controller: 'LoginController'
        }).when('/sessions', {
            templateUrl: appBaseUrl + '/sessions/sessions.html',
            controller: 'SessionsController',
            controllerAs: 'sessions'
        }).when('/sessions/:id', {
            templateUrl: appBaseUrl + '/sessions/session-info.html',
            controller: 'SessionInfoController',
            controllerAs: 'sessionInfo'
        }).when('/keys', {
            templateUrl: appBaseUrl + '/keys/keys.html',
            controller: 'KeysController',
            controllerAs: 'keys'
        }).when('/key-details/:id', {
            templateUrl: appBaseUrl + '/key-details/key-details.html',
            controller: 'KeyDetailsController'
        }).when('/keys/search', {
            templateUrl: appBaseUrl + '/search-keys/keys-search-form.html',
            controller: 'KeysSearchController',
            controllerAs: 'keysSearch'
        }).when('/users', {
            templateUrl: appBaseUrl + '/users/users.html',
            controller: 'UsersController',
            controllerAs: 'users'
        }).when('/user-details/:id', {
            templateUrl: appBaseUrl + '/user-details/user-details.html',
            controller: 'UserDetailsController'
        }).when('/users/search', {
            templateUrl: appBaseUrl + '/search-users/users-search-form.html',
            controller: 'UsersSearchController',
            controllerAs: 'usersSearch'
        }).when('/users/register', {
            templateUrl: appBaseUrl + '/forms/user-form.html',
            controller: 'UserRegisterController'
        }).when('/keys/register', {
            templateUrl: appBaseUrl + '/forms/key-form.html',
            controller: 'KeyRegisterController'
        }).when('/users/edit/:id', {
            templateUrl: appBaseUrl + '/forms/user-form.html',
            controller: 'UserEditController'
        }).when('/keys/edit/:id', {
            templateUrl: appBaseUrl + '/forms/key-form.html',
            controller: 'KeyEditController'
        }).when('/keys/seed', {
            templateUrl: appBaseUrl + '/keys-seed/keys-seed.html',
            controller: 'KeysSeedController',
            controllerAs: 'keysSeed'
        }).otherwise({redirectTo: '/home'});
    }
})();
