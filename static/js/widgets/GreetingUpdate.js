define([
	"dojo/_base/declare",
	"dojo/dom",
	"dojo/dom-style",
	"dijit/_Widget",
	"dijit/ConfirmDialog",
	"dojo/request",
	"dojo/cookie",
	"widgets/Greeting"
], function (declare, dom, domStyle, _Widget, ConfirmDialog, request, cookie, Greeting) {
	return declare([_Widget, ConfirmDialog], {
		title: "Create Greeting Window",
		constructor: function(greeting) {
			var contentWidget = new Greeting(greeting);
			//contentWidget.startup();
			this.content = contentWidget;
		},
		postCreate: function () {
			this.inherited(arguments);
		},
		onExecute: function(){
			var content = this.content.greetingContentNode.value;
			var greetingName = this.content.greetingNameNode.value;
			var url = this.url;
			request(url, {
				method: 'PUT',
				data: JSON.stringify({'content': content, 'greetingName': greetingName}),
				headers: {
					"Content-Type": 'application/json; charset=utf-8',
					"Accept": "application/json",
					"X-CSRFToken": cookie("csrf_token")}
			}).then(function(data){
				console.log(data);
			},function(err){
				console.log(err);
			});
		}
	});
});
