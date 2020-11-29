var slideindex = 1;
window.onload = function(){show_slides(slideindex);}

function plus_slides(n){
    show_slides(slideindex += n);
}

function currentSlide(n){
    show_slides(slideindex = n)
}

function show_slides(n){
    var i;
    var slides = document.getElementsByClassName("mystock-slide")
    var dots = document.getElementsByClassName("dot");
    if (n > slides.length){slideindex = 1}
    if (n < 1){slideindex = slides.length}
    for(i = 0; i < dots.length; i++){
        dots[i].className = dots[i].className.replace(" active","");
    }
    for (i = 0; i < slides.length; i++){
        slides[i].style.display = "none"
    }
    slides[slideindex-1].style.display = "inline-block";
    dots[slideindex-1].className += " active"
}


