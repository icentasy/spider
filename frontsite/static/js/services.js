// services.js
var mServices = angular.module("mServices", [])

.factory('userService',['$http', 'PostCfg', function($http,PostCfg){
	return {
		logout: function(user){
      $http.post("/MeetingMng/api/v1/companyManagerLogout", user, PostCfg)
      .success(function(data){
        $cookieStore.remove("username");
        window.location.href = "/MeetingMng";
      });
    }
	};
}])

.constant('PostCfg',{
  headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
  transformRequest: function(data) {
      return $.param(data);
  }
})

.constant("Category",{
  list:[{type:'meishitianxia', name:'美食'},
  {type:'wanggoujingpin', name:'网购'},
  {type:'dianyingzhanlan', name:'电影'},
  {type:'shenghuoyule', name:'娱乐'},
  {type:'jiudian', name:'酒店'},
  {type:'lvyou', name:'旅游'}
  ]
})
