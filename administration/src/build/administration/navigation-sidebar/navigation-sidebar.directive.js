(function () {
    'use-strict';

    angular
        .module('administration')
        .directive('navigationSidebar', navigationSidebar);

    navigationSidebar.$inject = ['templateServiceProvider'];
    function navigationSidebar(templateServiceProvider) {
        var appBaseUrl = templateServiceProvider.appBaseUrl();
        return {
            retstrict: 'E',
            scope: false,
            controller: 'SidebarController',
            templateUrl: appBaseUrl + '/navigation-sidebar/navigation-sidebar.html'
        }
    }
})();