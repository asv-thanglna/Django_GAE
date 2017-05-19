
define([
		"dojo/_base/declare",
		"dojo/_base/lang",
		"dojo/_base/array",
		"dojo/on",
		"dojo/request/xhr",
		"dojo/cookie",
		"dijit/_WidgetBase",
		"dijit/_TemplatedMixin",
		"dojo/text!./templates/GreetingsWidget.html"
	], function(declare, lang, arrayUtil, on, xhr, cookie, _WidgetBase, _TemplatedMixin, template){
	return declare("GreetingWidget", [_WidgetBase, _TemplatedMixin],{
		greetingName: 'No name',
		author: "An anonymous person",
		deleteUrl: require.toUrl("../static/img/delete.png"),
		updateUrl: require.toUrl("../static/img/update.png"),
		templateString: template,
		baseClass: "greetingWidget",

		postCreate: function(){
			this.inherited(arguments);
			this.own(
				on(this.deleteUrlNode, 'click', lang.hitch(this, "_deleteGreeting")),
				on(this.updateUrlNode, 'click', lang.hitch(this, "_updateGreeting"))
			)
		},

		_setDeleteUrlAttr: function(imagePath){
			if (imagePath != ''){
				this._set("deleteUrl", imagePath);
				this.deleteUrlNode.src = imagePath;
			}
		},

		_setUpdateUrlAttr: function(imagePath){
			if (imagePath != ''){
				this._set("updateUrl", imagePath);
				this.updateUrlNode.src = imagePath;
			}
		},

		_showGreetingDetail: function(){

		},

		_updateGreeting: function(){
			this._showGreetingDetail()
		},

		_deleteGreeting: function(){
			if(confirm("Are you sure?")){
				xhr.del(this.url, {
					headers: {
						"Content-Type": 'application/json; charset=utf-8',
						"Accept": "application/json",
						"X-CSRFToken": cookie("csrf_token")
					}
				}).then(function(data){
					console.log(data);
				}, function(error){
					console.log("error")
				});
			}
		}
	})
});
