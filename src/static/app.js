angular.module('ui.bootstrap.demo', ['ngAnimate', 'ui.bootstrap']);
angular.module('ui.bootstrap.demo').controller('TypeaheadCtrl', function($scope, $http, $sce) {

	$scope.getChi = function(val) {

		if (val.indexOf(' ') === -1) {
			return $http.get('/api/prefixChi', {
				params: {
					word: val
				}
			}).then(function(response){
				r = response.data.results.map(function(item){
					return item;
				});
				return r;
			}); 
		} else {
			return $http.get('/api/chi', {
				params: {
					word: val
				}
			}).then(function(response){
				r = response.data.results.map(function(item){
					return item;
				});
				return r;
			});
		}

		angular.element('#searchChi').controller('ngModel').$setViewValue($scope.chiModel);
		angular.element('#searchChi').controller('ngModel').$render();
	};

	$scope.getMv = function(val) {

		if (val.indexOf(' ') === -1) {
			return $http.get('/api/prefixMv', {
				params: {
					word: val
				}
			}).then(function(response){
				r = response.data.results.map(function(item){
					return item;
				});
				return r;
			}); 
		} else {
			return $http.get('/api/mv', {
				params: {
					word: val
				}
			}).then(function(response){
				r = response.data.results.map(function(item){
					return item;
				});
				return r;
			});
		}

		angular.element('#searchMv').controller('ngModel').$setViewValue($scope.mvModel);
		angular.element('#searchMv').controller('ngModel').$render();
	};

	$scope.onChangeChi = function(){
		angular.element('#searchChi').controller('ngModel').$setViewValue(val);
		angular.element('#searchChi').controller('ngModel').$render();
	}

	$scope.onChangeMv = function(){
		angular.element('#searchMv').controller('ngModel').$setViewValue(val);
		angular.element('#searchMv').controller('ngModel').$render();
	}

	$scope.onSelectChi = function ($item, $model, $label) {
		if($scope.chiModel.indexOf(' ') > -1){
			$scope.getArticles('chi');
			return;
		}

		$scope.chiModel += ' ';
		$scope.getChi($scope.chiModel);

		//no clue how this works, but it allows the UI to make a request when a value is selected
		angular.element('#searchChi').controller('ngModel').$setViewValue($scope.chiModel);
		angular.element('#searchChi').controller('ngModel').$render();
	};

	$scope.onSelectMv = function ($item, $model, $label) {
		if($scope.mvModel.indexOf(' ') > -1){
			$scope.getArticles('mv');		
			return;
		}

		//if there's no space in the input, add a space so that prefix recommendation works
		$scope.mvModel += ' ';
		$scope.getMv($scope.mvModel);

		//no clue how this works, but it allows the UI to make a request when a value is selected
		angular.element('#searchMv').controller('ngModel').$setViewValue($scope.mvModel);
		angular.element('#searchMv').controller('ngModel').$render();
	};

	$scope.getArticles = function(algorithm) {
		if(algorithm == 'chi'){
			return $http.get('/api/searchBigrams', {
				params: {
					query: $scope.chiModel
				}
			}).then(function(response){
				$scope.chiArticles = response.data.results;	
			});
		} else if (algorithm == 'mv'){
			return $http.get('/api/searchCollocs', {
				params: {
					query: $scope.mvModel
				}
			}).then(function(response){
				$scope.mvArticles = response.data.results;
			});
		}
	};

	$scope.getHtmlTitle = function(article){
		if(!article.highlight)
			return $sce.trustAsHtml(article.text);
		return $sce.trustAsHtml(article.highlight.text ? article.highlight.text[0] : article.text);
	};
});
