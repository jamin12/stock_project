var slideindex = 1;
show_slide(slideindex);

function plus_slides(n){
    show_slide(slideindex += n);
}


function show_slide(n){
    var i;
    var slides = document.getElementsByClassName("mystock-slide")
    if (n > slides.length){slideindex = 1;}
    if (n < 1){slideindex = slides.length;}
    for (i = 0; slides.length; i++){
        slides[i].style.display = "none";
    }
    slides[slideindex-1].style.display = "block";
}

