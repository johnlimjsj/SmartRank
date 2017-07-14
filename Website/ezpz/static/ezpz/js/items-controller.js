(function(){
	var controller = function($scope, $log, $location, $route, ezpzItemsService){
		$scope.goodsData = {};
		$scope.servicesData = {};
		$scope.errorMessage = "";
		var vm = this;

		// on startup, get the topics and get the number of pages
		vm.activate = function(){

			

			// getGoodsData();
			// getServicesData();
		};

		function getGoodsData(){
			ezpzItemsService.getGoodsData($scope.pageNumber, function(response){
				if (response.success){
					$scope.goodsData = response.goodsData.data.results;
					$scope.errorMessage = "";
				} else {
					$scope.errorMessage += " Unable to retrieve goods data from server.";
				}
			});
		}

		function getServicesData(){
			ezpzItemsService.getServicesData($scope.pageNumber, function(response){
				if (response.success){
					$scope.servicesData = response.servicesData.data.results;
					$scope.errorMessage = "";
				} else {
					$scope.errorMessage += " Unable to retrieve services data from server.";
				}
			});
		}

		vm.activate();

	};

	var module = angular.module('ezpzMain');
	module.controller('ezpzItemsController', ['$scope', '$log', '$location', '$route', 'ezpzItemsService', controller]);
})();