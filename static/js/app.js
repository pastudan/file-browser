angular.module('browserApp', [])
    .service('dataService', function($http) {
        this.get_files = function(directory){
            return $http.get('/api/v1.0/files/'+directory);
        }
    })

    .controller('BrowserController', function($scope, dataService) {

        $scope.get_files = function(directory){
            directory = directory || ''
            dataService.get_files(directory).then(function(files) {
                console.log(files.data)
                $scope.files = files.data;
            });
        };

        $scope.get_files()
    });