(function(){
	var service = function($log, $http){

		// encode the data with content type application/x-www-form-urlencoded
		var formURLEncode = function(obj) {
	        var str = [];
	        for(var p in obj)
	        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
	        return str.join("&");
	    };

	    var header = {'Content-Type': 'application/x-www-form-urlencoded'};

	    // exposes these functions as part of this service
		return {
			formURLEncode: formURLEncode,
			header: header
		};

	};

	var module = angular.module('ezpzMain');
	module.factory('ezpzServerService', ['$log', '$http', service]);
})();
