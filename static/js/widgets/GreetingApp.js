
define([
		"dojo/_base/array",
		"dojo/dom",
		"dojo/request/xhr",
		'dojo/ready',
		"widgets/GreetingsWidget"
	], function(arrayUtil, dom, xhr, ready, GreetingsWidget){
		var loadGreetings = function(){
			xhr.get("/api/v1/default_guestbook/greetings/?limit=10", {
				handleAs: "json"
			}).then(function(data){
				var greetingContainer = dom.byId("greetingContainer");
				arrayUtil.forEach(data.greetings, function(greeting){
					var widget = new GreetingsWidget(greeting).placeAt(greetingContainer);
				});
			});
		};
	return function(){
		ready(function() {
			loadGreetings();
		});
	};
});
