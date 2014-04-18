var loaders = [];

function loaded()
{
	for(loader in loaders){
		loaders[loader]();
	}
}



function nodeListIter(list_query, func){
    var list = document.querySelectorAll(list_query);
    for(var i = 0; i < list.length; i++){
        func(list[i], i, list);
    }
}


function previous_sibling(node){
	prev_sib = node.previousSibling;
	if(prev_sib.nodeName == "#text"){
		return previous_sibling(prev_sib);
	} else {
		return prev_sib;
	}
}

function next_sibling(node){
	next_sib = node.nextSibling;

	if(next_sib.nodeName == "#text"){
		return next_sibling(next_sib);
	} else {
		return next_sib;
	}
}

String.prototype.repeat = function( num )
{
    return new Array( num + 1 ).join( this );
}