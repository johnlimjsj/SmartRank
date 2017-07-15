(function(){
	var app = angular.module('ezpzMain', ['ngRoute']);

	var controller = function($scope, $log){
		var vm = this;
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
		.when("/analytics", {
			templateUrl: "static/ezpz/templates/analytics.html",
			controller: "ezpzAnalyticsController"
		})
		.otherwise({
			templateUrl: "static/ezpz/templates/items.html",
			controller: "ezpzItemsController"
		})
	})

	app.controller('ezpzMainController', ['$scope', '$log', controller]);
})();