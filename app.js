var app = angular.module('pepExplorer', []);
app.controller('pepCtrl', function($scope, $http) {
    $scope.selected_status = 'Any';
    $scope.selected_version = 'Any';
    var v = Date.now();
    $http.get("index.json?cache-bust=" + v)
    .then(function (response) {
        $scope.peps = response.data.peps;
        $scope.possible_python_versions = response.data.possible_python_versions;
        $scope.possible_statuses = response.data.possible_statuses;
    });

    $scope.pickversion = function(x){
        $scope.selected_version = x;
    };
    $scope.pickstatus = function(x){
        $scope.selected_status = x;
    };
});
