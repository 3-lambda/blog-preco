'use strict'

let myApp = angular.module('BlogApp', [])

myApp.controller('BlogCtrl',
	function($scope, $http) {

		$scope.addLead = function(){
			console.log('cu')
			$http({
				method: 'POST',
				url: '/insert_lead',
				data: {
					form: $scope.form
				}
			})
		}

		$scope.addConteudo = function(){
			$http({
				method: 'POST',
				url: '/insert_conteudo',
				data: {
					form: $scope.form
				}
			})
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

		$scope.show_post = function() {
			$http({
				method: 'GET',
				url: '/get_post/<int:post_id>'
			}).then(function(response) {
				$scope.post = response.data
			}, function(error) {
				console.log(error)
			})
		}


		$scope.show_leads = function() {
			$http({
				method: 'GET',
				url: '/get_leads'
			}).then(function(response) {
				$scope.leads = response.data
			}, function(error) {
				console.log(error)
			})
		}

		$scope.show_leads()
		$scope.show_posts()
	}
)
.config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('//').endSymbol('//')
    })
