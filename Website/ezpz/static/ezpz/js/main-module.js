(function(){
	var app = angular.module('ezpzMain', ['ngRoute']);

	var controller = function($scope, $log){
		var vm = this;

		// var video = document.querySelector('video');
		// var canvas = document.querySelector('canvas');
		// var ctx = canvas.getContext('2d');
		// var localMediaStream = null;

		// function snapshot() {
		// 	if (localMediaStream) {
		// 		ctx.drawImage(video, 0, 0);
		// 		// "image/webp" works in Chrome.
		// 		// Other browsers will fall back to image/png.
		// 		document.querySelector('img').src = canvas.toDataURL('image/webp');
		// 	}
		// }

		// function errorCallback(){
		// console.log("Error");
		// }

		// video.addEventListener('click', snapshot, false);

		// // Not showing vendor prefixes or code that works cross-browser.
		// navigator.getUserMedia({video: true}, function(stream) {
		// video.src = window.URL.createObjectURL(stream);
		// localMediaStream = stream;
		// }, errorCallback);
		
	};

	// application configuration, enables things such as $log.debug and removes the need for django's csrf_token by using angular's
	app.config(function($locationProvider, $logProvider, $httpProvider) {
	    $locationProvider.html5Mode(true);
	    $logProvider.debugEnabled(true)
	    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
		$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	});

	// routing on the client side
	app.config(function($routeProvider, $locationProvider){
		$routeProvider
		.when("/", {
			templateUrl: "static/ezpz/templates/items.html",
			controller: "ezpzItemsController"
		})
		.when("/goods", {
			templateUrl: "static/ezpz/templates/items.html",
			controller: "ezpzItemsController"
		})
		.when("/createGoods", {
			templateUrl: "static/ezpz/templates/createGoods.html",
			controller: "ezpzCreateGoodsController"
		})
		.when("/createServices", {
			templateUrl: "static/ezpz/templates/createServices.html",
			controller: "ezpzCreateServicesController"
		})
		.otherwise({
			templateUrl: "static/ezpz/templates/items.html",
			controller: "ezpzItemsController"
		})
	})

	app.controller('ezpzMainController', ['$scope', '$log', controller]);
})();