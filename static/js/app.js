angular.module('browserApp', [])
    .service('dataService', function($http) {
        this.get_files = function(fullPath){
            return $http.get('/api/v1.0/files/'+fullPath);
        }
    })

    .controller('BrowserController', function($scope, dataService) {

        $scope.path = [];
        $scope.showHidden = false;

        $scope.navigate_path = function(index){
            $scope.path = $scope.path.slice(0, index);
            var fullPath = $scope.path.join('/');
            $scope.open_directory(fullPath)
        };

        $scope.open_directory = function(directory, pushToPath){
            //todo: history.pushState so  back button works
            directory = directory || '';
            if (directory != '' && pushToPath){
                $scope.path.push(directory)
            }
            var fullPath = $scope.path.join('/');
            dataService.get_files(fullPath).then(function(items) {
                $scope.items = items.data;
            });
        };

        $scope.open_directory()
    });