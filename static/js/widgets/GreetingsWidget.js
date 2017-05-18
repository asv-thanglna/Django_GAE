
define([
		"dojo/_base/declare",
		"dojo/_base/fx",
		"dojo/_base/lang",
		"dojo/_base/array",
		"dojo/dom",
		"dojo/dom-style",
		"dojo/mouse",
		"dojo/on",
		"dojo/request",
		"dojo/cookie",
		"dijit/_WidgetBase",
		"dijit/_TemplatedMixin",
		"dijit/ConfirmDialog",
		"dojo/text!./templates/GreetingsWidget.html",
		"widgets/GreetingUpdate"
	], function(declare, baseFx, lang, arrayUtil, dom, domStyle, mouse, on, request, cookie, _WidgetBase, _TemplatedMixin, ConfirmDialog, template, GreetingUpdate){
	return declare("GreetingWidget", [_WidgetBase, _TemplatedMixin],{
		greetingName: 'No name',
		author: "An anonymous person",
		deleteUrl: require.toUrl("../static/img/delete.png"),
		updateUrl: require.toUrl("../static/img/update.png"),
		templateString: template,
		baseClass: "greetingWidget",
		mouseAnim: null,
		baseBackgroundColor: "#fff",
		mouseBackgroundColor: "#def",
		postCreate: function(){
			var domNode = this.domNode;
			this.inherited(arguments);
			domStyle.set(domNode, "backgroundColor", this.baseBackgroundColor);
			this.own(
				on(domNode, mouse.enter, lang.hitch(this, "_changeBackground", this.mouseBackgroundColor)),
				on(domNode, mouse.leave, lang.hitch(this, "_changeBackground", this.baseBackgroundColor))
			)
		},
		_changeBackground: function(newColor){
			if (this.mouseAnim){
				this.mouseAnim.stop();
			}
			this.mouseAnim = baseFx.animateProperty({
				node: this.domNode,
				properties: {
					backgroundColor: newColor
				},
				onEnd: lang.hitch(this, function(){
					this.mouseAnim = null;
				})
			}).play();
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
			var greeting = {
				greetingName: this.greetingName,
				url: this.url,
				greetingContent: this.content};
			var greetingdetail = new GreetingUpdate(greeting);
			greetingdetail.startup();
			greetingdetail.show();
		},
		_updateGreeting: function(){
			this._showGreetingDetail()
		},
		_deleteGreeting: function(e){
			var url = this.url;
			var dialog = new ConfirmDialog({
				title: "Remove Greeting Confirm",
				content: "Do you want to remove this Greeting?",
				style: "width: 600px",
				onExecute: function(){
					request(url, {
						method: 'DELETE',
						headers: {
							"Content-Type": 'application/json; charset=utf-8',
							"Accept": "application/json",
							"X-CSRFToken": cookie("csrf_token")
						}
					}).then(function(data){

					},function(err){
						console.log(err);
					});
				}
			});
			dialog.show();
		}
	})
});