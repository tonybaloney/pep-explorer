var app = angular.module('pepExplorer', []);
app.controller('pepCtrl', function($scope, $http) {
    $scope.selected_status = 'Any';
    $scope.selected_version = 'Any';
    $http.get("index.json")
    .then(function (response) {
        $scope.peps = response.data.peps;
        $scope.possible_python_versions = response.data.possible_python_versions;
        $scope.possible_statuses = response.data.possible_statuses;
    });
});
app.filter('pepFilter', function($scope) {
    return function(x) {
        return x;
    }});