(function(){
	var service = function($log, $http, ezpzServerService){

		// creates a new topic
		var createServices = function(data, callback){

			var url = "api/services/";

			// sends the data over to the server to create a new topic
			$http({
				method: 'POST',
				url: url,
				headers: ezpzServerService.header,
			    transformRequest: ezpzServerService.formURLEncode,
			    data: data
			})
			.then(successCallback, errorCallback);

			// on success
			function successCallback(response){
				$log.debug("createServices success");
				callback({
					success:true
				});
			}

			// on error
			function errorCallback(response){
				$log.debug("createServices fail");
				callback({
					success:false
				})
			}

		};

		var uploadFeedback = function(data, callback){
			var url = "store-feedback/";

			// sends the data over to the server to create a new topic
			$http({
				method: 'POST',
				url: url,
				// headers: ezpzServerService.header,
			 //    transformRequest: ezpzServerService.formURLEncode,
			    data: {
			    	'feedback': data
			    }
			})
			.then(successCallback, errorCallback);

			// on success
			function successCallback(response){
				$log.debug("Upload feedback success");
				callback({
					success:true
				});
			}

			// on error
			function errorCallback(response){
				$log.debug("Upload feedback fail");
				callback({
					success:false
				})
			}

		}


	    // exposes these functions as part of this service
		return {
			createServices: createServices,
			uploadFeedback: uploadFeedback,
		};

	};

	var module = angular.module('ezpzMain');
	module.factory('ezpzCreateServicesService', ['$log', '$http', 'ezpzServerService', service]);
})();