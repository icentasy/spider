
angular.module("spiderapp", ["ngRoute", "mControllers", "mDirectives", "mFilters", "mRoutes", "mServices"])
.factory('CategoryList', function(){
  return [{type:'meishitianxia', name:'美食'},
		  {type:'wanggoujingpin', name:'网购'},
		  {type:'dianyingzhanlan', name:'电影'},
		  {type:'shenghuoyule', name:'娱乐'},
		  {type:'jiudian', name:'酒店'},
		  {type:'lvyou', name:'旅游'}
  ];
})

.config(function($routeProvider) {
	$routeProvider.when('/', {
		templateUrl: 'home.html',
		controller: 'homeCtrl'
	}).when('/search', {
		templateUrl: 'search.html',
		controller: 'searchCtrl'
	}).otherwise({
		redirectTo: '/'
	});

})

