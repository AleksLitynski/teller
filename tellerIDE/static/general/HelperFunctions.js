//'script'
function helperIncludeInDocument(type, src){
	var imported = document.createElement(type);
	imported.src = src;
	document.head.appendChild(imported);
}