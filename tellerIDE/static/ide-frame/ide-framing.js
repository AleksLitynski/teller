loaders.push(function(){

    var vert_hor = "vert";
    var currentlyResizing = false;
    var a;
    var b;
    
    document.onmousemove = function(e){
        updateFold(e.clientX, e.clientY);
    }
    document.onmouseup = function(e){
        currentlyResizing = false;
    }



    nodeListIter( ".vert-handle, .hor-handle", function(element, index, array){
        element.onmousedown = function(){
            currentlyResizing = true;
            a = previous_sibling(element);
            b = next_sibling(element);
            if(element.classList.contains("hor-handle")){
                vert_hor = "hor";
            } else {
                vert_hor = "vert";
            }
        };
    });


    function updateFold(x, y){

        if(!currentlyResizing) return;

        if(vert_hor == "vert"){ //Top to Bottom

            a.style.width = "calc("+(     (x / window.innerWidth) * 100)+"% - 15px)";
            b.style.width = "calc("+((100-(x / window.innerWidth) * 100))+"% - 15px)";
        }
        
        if(vert_hor == "hor"){ //Left to Right
            a.style.height = "calc("+(     (y / window.innerHeight) * 100)+"% - 15px)";
            b.style.height = "calc("+((100-(y / window.innerHeight) * 100))+"% - 15px)";

        }

    }

})


