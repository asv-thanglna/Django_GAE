define([
	"dojo/_base/declare",
	"dojo/dom",
	"dojo/dom-style",
	"dijit/_Widget",
	"dijit/_TemplatedMixin",
	"dijit/_WidgetsInTemplateMixin",
	"dojo/text!./templates/GreetingDetail.html"
], function(declare, dom, domStyle, _Widget, _TemplatedMixin, _WidgetsInTemplateMixin, template){
	return declare([_Widget, _TemplatedMixin, _WidgetsInTemplateMixin], {
		templateString: template
	})
});