// controllers.js
var mControllers = angular.module("mControllers", [])
 


.controller("navbarCtrl", function($scope, $http) {
   $scope.currCity = '武汉';
   $scope.cities ={};
   //get citydata
   $http
   .get('http://0.0.0.0:5005/tuangou/city')
   .success(function(data, status){
   	// console.log(data)
   	if(data.status != 0) console.log(data.msg);

   	var cs = data.data;
   	var first_char = '';
   	for(var i=0; i<cs.length;i++){
   		first_char = cs[i].first_char;
   		if($scope.cities[first_char] == undefined){
   			$scope.cities[first_char] = [];
   			$scope.cities[first_char].push(cs[i]);
   		}
   		else{
   			$scope.cities[first_char].push(cs[i]);
   		}
   	}
   	// console.log($scope.cities);
   });
})

.controller("sidebarCtrl", function($scope, CategoryList) {
   $scope.list = CategoryList;

})

.controller("homeCtrl", function($scope, $http, $route, CurrCity) {

  $scope.category = $route.current.params.category || 'meishitianxia';
  $scope.order = $route.current.params.order || 1;
  $scope.page = parseInt($route.current.params.page) || 1;
  // console.log($route.current.params)
  CurrCity.pinyin = $route.current.params.city || CurrCity.pinyin;
  $http
  .get('http://localhost:5005/tuangou/deal/'+CurrCity.pinyin+'/'+$scope.category
    +'?order='+$scope.order+'&page='+$scope.page)
  .success(function(data, status){
    console.log(data.data.items.length)
    if(data.status != 0) console.log(data.msg);

    $scope.items = data.data.items;
    $scope.total = data.data.total;
    $scope.itemLoaded = true;
  });
})

.controller("searchCtrl", function($scope, $http, $route) {

  $scope.category = $route.current.params.category || 'meishitianxia';
  $scope.order = $route.current.params.order || 1;
  $scope.page = parseInt($route.current.params.page) || 1;
  // console.log($route.current.params)

  $http
  .get('http://localhost:5005/tuangou/deal/anshan/'+$scope.category
  	+'?order='+$scope.order+'&page='+$scope.page)
  .success(function(data, status){
  	// console.log(data)
  	console.log(data.data.items.length)
  	if(data.status != 0) console.log(data.msg);

  	$scope.items = data.data.items;
  	$scope.total = data.data.total;
  });
})

.constant("CurrCity",{
  // name:'anshan',
  pinyin:'wuhan'
})

