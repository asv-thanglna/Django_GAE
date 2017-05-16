
define([
		"dojo/_base/declare",
		"dojo/_base/fx",
		"dojo/_base/lang",
		"dojo/dom-style",
		"dojo/mouse",
		"dojo/on",
		"dijit/_WidgetBase",
		"dijit/_TemplatedMixin",
		"dojo/text!./templates/GreetingWidget.html"
	], function(declare, baseFx, lang, domStyle, mouse, on, _WidgetBase, _TemplatedMixin, template){
	return declare("GreetingWidget", [_WidgetBase, _TemplatedMixin],{
		greetingName: 'no name',
		content: "",
		author: "",
		updatedBy: "",
		updatedDate: "",
		date: "",
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
		}
	})
});