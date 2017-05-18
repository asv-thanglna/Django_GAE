define([
	"dojo/_base/declare",
	"dojo/dom",
	"dojo/dom-style",
	"dijit/_Widget",
	"dijit/_TemplatedMixin",
	"dijit/_WidgetsInTemplateMixin",
	"dojo/text!./templates/GreetingDetail.html",
	"dijit/ConfirmDialog",
	"dijit/form/Button",
	"dijit/form/TextBox"
], function (declare, dom, domStyle, _Widget, _TemplatedMixin, _WidgetsInTemplateMixin, template, ConfirmDialog) {
	return declare([_Widget, _TemplatedMixin, _WidgetsInTemplateMixin, ConfirmDialog], {
		//id: "new",
		title: "Create Greeting Window",
		//content: template,
		greetingName: "new greeting",
		greetingContent: "the content",
		constructor: function(greeting) {
			var contentWidget = new (declare( [ _Widget, _TemplatedMixin, _WidgetsInTemplateMixin ], {
				templateString: template,
				greetingName: greeting.greetingName,
				greetingContent: greeting.greetingContent
				//_setGreetingName: function(name){
				//	this._set("greetingName", name);
				//	this.greetingNameNode.value = name;
				//},
				//_setGreetingContent: function(content){
				//	this._set("greetingContent", content);
				//	this.greetingContentNode.value = content;
				//},
				//_getGreetingName: function(){
				//	return this.greetingNameNode.value;
				//},
				//_getGreetingContent: function(){
				//	return this.greetingContentNode.value;
				//}
			}));
			//contentWidget.startup();
			this.content = contentWidget;
		},
		postCreate: function () {
			this.inherited(arguments);
			console.log(this.greetingName);
			// make reference to widget from the node attachment
			//this.submitButton = dijit.getEnclosingWidget(this.ContentsubmitButtonNode);
			//// override its onSubmit
			//this.submitButton.onClick = function () {
			//	//alert("username :" + dom.byId("userId").value()
			//	//+ "  Password: " + dom.byId("password").value());
			//};
		},
		onExecute: function(){
			console.log(this.content.greetingContentNode.value);
			console.log(this.content.greetingNameNode.value);
		}
	});
});
