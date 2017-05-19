
define([
	"dojo/_base/declare",
	"dojo/_base/lang",
	"dojo/_base/array",
	"dojo/on",
	"dojo/dom-style",
	"dojo/request/xhr",
	"dojo/cookie",
	"dijit/_WidgetBase",
	"dijit/_TemplatedMixin",
	"dojo/text!./templates/GreetingsWidget.html"
	], function(declare, lang, arrayUtil, on, domStyle, xhr, cookie, _WidgetBase, _TemplatedMixin, template){
	return declare("GreetingWidget", [_WidgetBase, _TemplatedMixin],{
		greetingName: 'No name',
		author: "An anonymous person",
		deleteUrl: require.toUrl("../static/img/delete.png"),
		updateUrl: require.toUrl("../static/img/update.png"),
		templateString: template,
		baseClass: "greetingWidget",

		postCreate: function(){
			this.inherited(arguments);
			this._changeGreetingUpdateAndDetail(true);
			this.own(
				on(this.deleteUrlNode, 'click', lang.hitch(this, "_deleteGreeting")),
				on(this.updateUrlNode, 'click', lang.hitch(this, "_updateGreeting")),
				on(this.updateButtonNode, 'click', lang.hitch(this, function(){
					var greetingWidget = this;
					var newGreetingName = this.greetingNameNode.value;
					var newGreetingContent = this.contentNode.value;
					xhr.put(this.url, {
						data: JSON.stringify({
							greetingName: newGreetingName,
							content: newGreetingContent
						}),
						headers: {
							"Content-Type": 'application/json; charset=utf-8',
							"Accept": "application/json",
							"X-CSRFToken": cookie("csrf_token")
						}
					}).then(function(data){
						greetingWidget.greetingName = newGreetingName;
						greetingWidget.content = newGreetingContent;
						greetingWidget._changeGreetingUpdateAndDetail(true);
					}, function(error){
						console.log(error);
					});

				})),
				on(this.cancelButtonNode, 'click', lang.hitch(this, function(){
					this._changeGreetingUpdateAndDetail(true);
				}))
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

		_changeGreetingUpdateAndDetail: function(value){
			if (value){
				domStyle.set(this.greetingDetailNode, "display", "block");
				domStyle.set(this.greetingUpdateNode, "display", "None");
			}else{
				domStyle.set(this.greetingDetailNode, "display", "None");
				domStyle.set(this.greetingUpdateNode, "display", "block");
			}
		},

		_updateGreeting: function(){
			this._changeGreetingUpdateAndDetail(false);
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
