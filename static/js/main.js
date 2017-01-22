'use strict'

let myApp = angular.module('BlogApp', [])

myApp.controller('BlogCtrl',
	function($scope, $http) {
		$scope.addCliente = function(){
			$http({
				method: 'POST',
				url: '/insert_cliente',
				data: {
					form: $scope.form
				}
			})
			$scope.show_clientes()
		}

		$scope.addConteudo = function(){
			$http({
				method: 'POST',
				url: '/insert_conteudo',
				data: {
					form: $scope.form
				}
			})
			$scope.show_conteudo()
		}

		$scope.show_posts = function() {
			$http({
				method: 'GET',
				url: '/get_posts'
			}).then(function(response) {
				$scope.posts = response.data
			}, function(error) {
				console.log(error)
			})
		}

		$scope.show_clientes = function() {
			$http({
				method: 'GET',
				url: '/get_clientes'
			}).then(function(response) {
				$scope.clientes = response.data
			}, function(error) {
				console.log(error)
			})
		}

		$scope.show_clientes()
		$scope.show_posts()
	}
)
.config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('//').endSymbol('//')
    })
