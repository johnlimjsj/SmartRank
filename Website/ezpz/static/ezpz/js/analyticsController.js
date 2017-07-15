(function(){
	var controller = function($scope, $log,  $location){

		var vm = this;

		vm.activate();
	};

	var module = angular.module('ezpzMain');
	module.controller('ezpzAnalyticsController', ['$scope', '$log',  '$location', controller]);
})();