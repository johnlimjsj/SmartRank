(function(){
	var service = function($log, $http, ezpzServerService){

		// creates a new topic
		var createGoods = function(data, callback){

			var url = "api/goods/";

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
				$log.debug("createGoods success");
				callback({
					success:true
				});
			}

			// on error
			function errorCallback(response){
				$log.debug("createGoods fail");
				callback({
					success:false
				})
			}

		};

		var uploadImage = function(data, callback){
			var url = "image/";
			var fd = new FormData();
			fd.append("image", data);

			// sends the data over to the server to create a new topic
			$http({
				method: 'POST',
				url: url,
				data: fd,
			    transformRequest: angular.identity,
			    headers: {
			        'Content-Type': undefined
			    }
				// headers: ezpzServerService.header,
			    // transformRequest: ezpzServerService.formURLEncode,
			    // data: {
			    // 	imageFeedback: data
			    // }
			})
			.then(successCallback, errorCallback);

			// on success
			function successCallback(response){
				$log.debug("upload Image success");
				callback({
					success:true
				});
			}

			// on error
			function errorCallback(response){
				$log.debug("upload Image fail");
				callback({
					success:false
				})
			}
		}


	    // exposes these functions as part of this service
		return {
			createGoods: createGoods,
			uploadImage: uploadImage,
		};

	};

	var module = angular.module('ezpzMain');
	module.factory('ezpzCreateGoodsService', ['$log', '$http', 'ezpzServerService', service]);
})();