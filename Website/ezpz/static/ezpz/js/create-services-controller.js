(function(){
	var controller = function($scope, $log,  $location, ezpzCreateServicesService){
		$scope.errorMessage = "";
		$scope.successMessage = "";
		$scope.servicesCategory = "";
		$scope.servicesName = "";
		$scope.servicesPrice = "";
		$scope.servicesLikes = "";
		$scope.servicesRating = "";
		$scope.currentSpeech = "";
		var TOPIC_LENGTH_LIMIT = 255;
		var vm = this;
		var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition)();
		recognition.lang = 'en-US';
		recognition.interimResults = false;
		recognition.maxAlternatives = 5;
		recognition.onresult = function(event) {
			$scope.currentSpeech = event.results[0][0].transcript;
			$scope.$apply();
		};

		vm.activate = function(){
		}

		$scope.startListening = function(){
			recognition.start();
		}

		$scope.stopListening = function(){
			recognition.stop();
		}

		// create a topic
		$scope.createServices = function(){

				// sets a new topic with the topic text and 0 upvotes and downvotes
				var data = {
					category: $scope.servicesCategory,
					name: $scope.servicesName,
					price: $scope.servicesPrice,
					likes: $scope.servicesLikes.toString(),
					rating: $scope.servicesRating.toString(),
				};

				// create the topic with the help of ezpzCreateTopicService
				ezpzCreateServicesService.createServices(data, function(response){
					if (response.success){
						$scope.errorMessage = "";
						$scope.successMessage = "Services Successfully created!";

						//redirect back to main page
						$location.path('/');
					} else {
						$scope.errorMessage = "Failed to create services.";
					}
				})
			// } 
		};

		vm.activate();


	};

	var module = angular.module('ezpzMain');
	module.controller('ezpzCreateServicesController', ['$scope', '$log',  '$location', 'ezpzCreateServicesService', controller]);
})();