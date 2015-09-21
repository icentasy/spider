// directives.js
var mDirectives = angular.module("mDirectives", [])

mDirectives.directive("directive", function() {
	return {
		restrict: 'E',
		template: '<div>directive test</div>',
		replace: true
	}
})