(function(){
	var service = function($log, $http, ezpzServerService){

		// gets all the current goods
		var getGoodsData = function(pageNumber, callback){

			var url = "api/goods/"

			$http({
				method: 'GET',
				url: url
			})
			.then(successCallback, errorCallback);

			// on success
			function successCallback(response){
				$log.debug("getGoodsData success");
				callback({
					success: true,
					goodsData: response
				});
			}

			// on error
			function errorCallback(response){
				$log.debug("getGoodsData fail");
				callback({
					success: false,
					goodsData: response
				})
			}
		};

		// gets all the current goods
		var getServicesData = function(pageNumber, callback){

			var url = "api/services/"

			$http({
				method: 'GET',
				url: url
			})
			.then(successCallback, errorCallback);

			// on success
			function successCallback(response){
				$log.debug("getServicesData success");
				callback({
					success: true,
					servicesData: response
				});
			}

			// on error
			function errorCallback(response){
				$log.debug("getServicesData fail");
				callback({
					success: false,
					servicesData: response
				})
			}
		};


		// exposed functions as part of this service
		return {
			getGoodsData: getGoodsData,
			getServicesData: getServicesData
		}

	};

	var module = angular.module('ezpzMain');
	module.factory('ezpzItemsService', ['$log', '$http', 'ezpzServerService', service]);
})();