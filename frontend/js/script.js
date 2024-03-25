$(".main__input").on("focus", function(){
    $('.select').addClass("select_active");
})


var field = $('#list').find('.option');
// собственно поиск
$('.main__input').bind('keyup', function() {
    var q = new RegExp($(this).val(), 'ig');
 
    for (var i = 0, l = field.length; i < l; i += 1) {
        var option = $(field[i]),
            parent = option.parent();

        if ($(field[i]).text().match(q)) {
            if (parent.is('span')) {
                option.show();
                parent.replaceWith(option);
            }
        } else {
            if (option.is('.option') && (!parent.is('span'))) {
                option.wrap('<span>').hide();
            }
        }
    } 
});


$('.option').on('click', function(){
    $('.main__input').val($(this).text());
    $('input').focus();
});




const box = document.querySelector(".main__input");
const select = document.querySelector(".select");
document.addEventListener('click', (e) => {
    const click1 = e.composedPath().includes(box);
    const click2 = e.composedPath().includes(select);
    if(!click1 && !click2)
        $('.select').removeClass("select_active");

})


transition = async function(){
    let box = document.querySelector(".loader");
    box.style.display = "inline-block"

    
    const prompt = document.getElementById("prompt").value;

    // const filters = document.querySelector('.filters:checked');

    const checkboxes = document.getElementsByName('filter');
    const values = Array.from(checkboxes)
    .filter(checkbox => checkbox.checked)
    .map(checkbox => checkbox.value);

    const response = await fetch("/get_books", {
            method: "POST",
            headers: { "Accept": "application/json", "Content-Type": "application/json" },
            body: JSON.stringify({ 
                prompt: prompt,
                filters: values
            })
        });
    if (response.data) {
        window.sessionStorage.setItem('data', JSON.stringify(response.data));
    }
    else {
        console.log(response);
    }
    window.location.href = '/books';
    box.style.display = "none"
};

const el = document.getElementById('btn');

el.addEventListener('click', async function(){
    transition();
});

document.addEventListener('keyup', function(event){
    if(event.keyCode == 13 && document.getElementById("prompt").value != ''){
        transition();
    }
});

