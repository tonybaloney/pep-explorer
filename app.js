var app = angular.module('pepExplorer', []);
app.controller('pepCtrl', function($scope, $http) {
    $scope.selected_version = 'Any';
    $scope.selected_status = 'Any';

    window.addEventListener('popstate', function (e) {
        var state = e.state || {version: 'Any', status: 'Any'};
        $scope.selected_version = state.version;
        $scope.selected_status = state.status;
        $scope.$apply();
    });

    function state(fn) {
        fn(
            {version: $scope.selected_version, status: $scope.selected_status},
            null,
            ['#', $scope.selected_version, '_', $scope.selected_status].join('')
        );
    }

    $scope.pickversion = function(x) {
        $scope.selected_version = x;
        state(history.pushState.bind(history));
    };
    $scope.pickstatus = function(x) {
        $scope.selected_status = x;
        state(history.pushState.bind(history));
    };

    $http.get("index.json?cache-bust=" + Date.now())
    .then(function (response) {
        $scope.peps = response.data.peps;
        $scope.possible_python_versions = response.data.possible_python_versions;
        $scope.possible_statuses = response.data.possible_statuses;

        var match = location.hash && location.hash.match(/^#([^_]+)_(.+)$/);

        if (match[1] && $scope.possible_python_versions.indexOf(match[1]) >= 0) {
            $scope.selected_version = match[1];
        }
        if (match[2] && $scope.possible_statuses.indexOf(match[2]) >= 0) {
            $scope.selected_status = match[2];
        }

        state(history.replaceState.bind(history));
    });
});
