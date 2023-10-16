$('.search__panel__btn').on('click', function(){
    
    $(this).closest('div.search__panel').find('div.search__panel__list').toggleClass('search__panel__list_active');
    $(this).toggleClass('search__panel__btn_active');

    $(this).closest('div.search__panel').find('div.search__panel__list_active').addClass('search__panel__list_animation')
    let elem = document.querySelector('.search__panel__list_animation');
    let opac = 0;
    
    function loop() {
        elem.style.opacity = opac;
        if (opac < 1) {
            opac += 0.03;
        } else {
            window.cancelAnimationFrame(animationFrame);
        }
        animationFrame = requestAnimationFrame(loop);
    }
    let animationFrame = requestAnimationFrame(loop);
    $(this).closest('div.search__panel').find('div.search__panel__list_active').removeClass('search__panel__list_animation')



/* Идея!!! создать класс, прибавить его к search__panel__list, красиво вывести с функцией ниже, и потом удалить этот класс для дальнейшего использования его к другим элементам, используя $(this) */
    /* let elem = document.querySelector('.search__panel__list_active');
    let opac = 0;
    
    function loop() {
        elem.style.opacity = opac;
        if (opac < 1) {
            opac += 0.03;
        } else {
            window.cancelAnimationFrame(animationFrame);
        }
        animationFrame = requestAnimationFrame(loop);
    }
    let animationFrame = requestAnimationFrame(loop); */

/*     $('.search__panel_title').toggleClass('search__panel__list_active');  

    let elem = document.querySelector('.search__panel_title');
    let opac = 0;
    
    function loop() {
        elem.style.opacity = opac;
        if (opac < 1) {
            opac += 0.03;
        } else {
            window.cancelAnimationFrame(animationFrame);
        }
        animationFrame = requestAnimationFrame(loop);
    }
    let animationFrame = requestAnimationFrame(loop); */
});

/* $('.search__panel__btn_heading').on('click', function(){
    $('.search__panel_heading').toggleClass('search__panel__list_active'); 
    let elem = document.querySelector('.search__panel_heading');
    let opac = 0;
    
    function loop() {
        elem.style.opacity = opac;
        if (opac < 1) {
            opac += 0.03;
        } else {
            window.cancelAnimationFrame(animationFrame);
        }
        animationFrame = requestAnimationFrame(loop);
    }
    let animationFrame = requestAnimationFrame(loop); 
}); */


/* Проверка работы oninput */
/* 
var inputTextField = document.getElementById('textField');
var outputTextField = document.getElementById('textResult');

inputTextField.oninput = function() {
    outputTextField.value = inputTextField.value;
}; */