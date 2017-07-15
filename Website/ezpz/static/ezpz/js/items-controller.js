(function(){
	var controller = function($scope, $log, $location, $route, ezpzItemsService){
		$scope.goodsData = {};
		$scope.servicesData = {};
		$scope.feedback = {};
		$scope.imageFeedback = {};
		$scope.errorMessage = "";
		var vm = this;

		// on startup, get the topics and get the number of pages
		vm.activate = function(){
			getFeedback();
			getImageFeedback();

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

		function getFeedback(){
			ezpzItemsService.getFeedback(function(response){
				if(response.success){
					$scope.feedback = response.feedback.feedback;
					$scope.errorMessage = "";
				} else {
					$scope.errorMessage += "Unable to retrieve feedback from server.";
				}
			});

		}

		function getImageFeedback(){
			ezpzItemsService.getImageFeedback(function(response){
				if(response.success){
					$scope.imageFeedback = response.images.images;
					console.log("string" + $scope.imageFeedback);
					$scope.errorMessage = "";
					$scope.$apply();
				} else {
					$scope.errorMessage += "Unable to retrieve image feedback from server.";
				}
			});
		}

		vm.activate();

	};

	var module = angular.module('ezpzMain');
	module.controller('ezpzItemsController', ['$scope', '$log', '$location', '$route', 'ezpzItemsService', controller]);
})();