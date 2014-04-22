state().loaded(function(){


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

        var percent = (x / window.innerWidth) * 100;
        if(vert_hor == "hor"){
            percent = (y / window.innerHeight) * 100;
        }

        if(a.classList.contains("left-column")){//central
            state().framing().central( percent );
        } else {
            if(a.parentNode.classList.contains("left-column")){//left
                state().framing().left( percent );
            }
            if(a.parentNode.classList.contains("right-column")){//right
                state().framing().right( percent );
            }
        }
    }

    state().framing().central(function(percent){
        document.querySelector(".left-column").style.width = "calc("+(percent)+"% - 15px)";
        document.querySelector(".right-column").style.width = "calc("+(100-percent)+"% - 15px)";
        return true;
    })
    state().framing().left(function(percent){
        document.querySelector(".left-column .top-row").style.height = "calc("+(percent)+"% - 15px)";
        document.querySelector(".left-column .bottom-row").style.height = "calc("+(100-percent)+"% - 15px)";
        return true;
    })
    state().framing().right(function(percent){
        document.querySelector(".right-column .top-row").style.height = "calc("+(percent)+"% - 15px)";
        document.querySelector(".right-column .bottom-row").style.height = "calc("+(100-percent)+"% - 15px)";
        return true;
    })



})


