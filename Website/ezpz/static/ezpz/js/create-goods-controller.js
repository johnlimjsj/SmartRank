(function(){
	var controller = function($scope, $log,  $location, ezpzCreateGoodsService){
		$scope.errorMessage = "";
		$scope.successMessage = "";
		$scope.goodsCategory = "";
		$scope.goodsName = "";
		$scope.goodsPrice = "";
		$scope.goodsLikes = "";
		$scope.goodsRating = "";
		var TOPIC_LENGTH_LIMIT = 255;
		var vm = this;


		var player = document.getElementById('player'); 
		var snapshotCanvas = document.getElementById('snapshot');
		var captureButton = document.getElementById('capture');

		var handleSuccess = function(stream) {
			// Attach the video stream to the video element and autoplay.
			player.srcObject = stream;
		};

		$scope.capture = function(){
			var context = snapshot.getContext('2d');
			// Draw the video frame to the canvas.
			context.drawImage(player, 0, 0, snapshotCanvas.width, 
				snapshotCanvas.height);
		}

		navigator.mediaDevices.getUserMedia({video: true})
			.then(handleSuccess);

		vm.activate = function(){
		}

		// create a topic
		$scope.createGoods = function(){

				// sets a new topic with the topic text and 0 upvotes and downvotes
				var data = {
					category: $scope.goodsCategory,
					name: $scope.goodsName,
					price: $scope.goodsPrice.toString(),
					likes: $scope.goodsLikes.toString(),
					rating: $scope.goodsRating.toString(),
				};

				// create the topic with the help of ezpzCreateTopicService
				ezpzCreateGoodsService.createGoods(data, function(response){
					if (response.success){
						$scope.errorMessage = "";
						$scope.successMessage = "Goods Successfully created!";

						//redirect back to main page
						$location.path('/');
					} else {
						$scope.errorMessage = "Failed to create goods.";
					}
				})
			// } 
		};

		vm.activate();
	};

	var module = angular.module('ezpzMain');
	module.controller('ezpzCreateGoodsController', ['$scope', '$log',  '$location', 'ezpzCreateGoodsService', controller]);
})();