/*
Name: Michael Blume
Georgian Digital Text Collective

This file was created for the Georgian Digital Text Collective. It will contain various methods for doing stuff to texts eventually!
*/

(function() {	
	"use strict";
	var qs = function(id){return document.querySelector(id);};
	var qsa = function(id){return document.querySelectorAll(id);};
	window.onload = function() {
		setup();
	};
	function setup() {
		$("#headerTest").load("header.html");
		$("#footerTest").load("footer.html");
	}
})();