$('.search__panel__btn').on('click', function(){
    
    $(this).closest('div.search__panel').find('div.search__panel__list').toggleClass('search__panel__list_active');
    $(this).toggleClass('search__panel__btn_active');

    /* создание класса для его анимации и последующее его удаление для анимации*/
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
});



/* Проверка работы oninput */
/* 
var inputTextField = document.getElementById('textField');
var outputTextField = document.getElementById('textResult');

inputTextField.oninput = function() {
    outputTextField.value = inputTextField.value;
}; */