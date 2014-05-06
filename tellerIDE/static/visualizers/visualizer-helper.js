var visualizerHelper = {
	getTab : function(tag){
		console.log("visualizerHelper::hi getTab");
		return document.querySelector("[data-vistype='"+tag+"']");

	},
	getBody:function(name){
		console.log("visualizerHelper::getBody");  
		return document.querySelector("[class='"+name+"']");
	}

};