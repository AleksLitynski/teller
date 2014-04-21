/*
	Function that *should be* part of javascript nativly,
	but don't warent an entire library to add their functionality.
*/

//Lets you itterate the result of a querySelectorAll query
function nodeListIter(list_query, func){
    var list = document.querySelectorAll(list_query);
    for(var i = 0; i < list.length; i++){
        func(list[i], i, list);
    }
}

//Gets the previous sibling that ISN'T a text node (ie: white space)
function previous_sibling(node){
	prev_sib = node.previousSibling;
	if(prev_sib.nodeName == "#text"){
		return previous_sibling(prev_sib);
	} else {
		return prev_sib;
	}
}

//Gets the next sibling that ISN'T a text node (ie: white space)
function next_sibling(node){
	next_sib = node.nextSibling;

	if(next_sib.nodeName == "#text"){
		return next_sibling(next_sib);
	} else {
		return next_sib;
	}
}

//Concats a string to itself X times.
String.prototype.repeat = function( num )
{
    return new Array( num + 1 ).join( this );
}