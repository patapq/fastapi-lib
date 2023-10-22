let array = ['Пушкин', 'Достоевский', 'Толстой'];

let sel = document.getElementById('choiced'); /* элемент select */

for (let index = 0; index < array.length; index++) {
    let opt = array[index]; /* присвоить значение списка */
    let el = document.createElement("option"); /* Создаем option */
    el.text = String(opt); /* Значение в строке выбора */
    el.value = String(opt); /* Значение передающееся на сервер */
    sel.add(el, null); /* Добавление option */
}




let element = document.querySelector('.js-choice');

const choices = new Choices(element,{
    searchEnabled: true
});

$('input').attr('name', 'prompt');
$('input').attr('id', 'prompt');

/* Не получается реализовать */
/* $('.main__clear').on('click', function(){
    $('.choices__item--selectable').remove();
    $('input[type=text]').val("");
    $('.choices__input--cloned').focus();
}); */


// Событие когда элемент получил фокус
$('.choices__input--cloned').focus(function(){
    document.querySelector(".choices__input--cloned").placeholder = "";

});

// Когда элемент теряет фокус
$('.choices__input--cloned').blur(function(){
	document.querySelector(".choices__input--cloned").placeholder = "Поиск книг по названию, автору и т.д.";
    document.querySelector(".choices__input--cloned").style = "min-width: 1ch; width: 30ch;"; 
});



// const el = document.getElementById('btn');
// console.log(el);
// console.log('HI!')

// el.addEventListener('click', async function(){
 
//     // const prompt = document.getElementById("prompt").value;
//     const info = document.getElementById("prompt").value;
    
    
//     // console.log(prompt);
//     console.log(info);

//     const response = await fetch("/books", {
//             method: "POST",
//             // redirect: "follow",
//             headers: { "Accept": "application/json", "Content-Type": "multipart/form-data" },
//             body: info
            
//         }).then(res => res.json());
//         // if (response.ok) {
//         //     const data = await response.json();
//         //     // document.getElementById("bebra").textContent = data.message;
//         //     // return data;
//         // }
//         // else
//         //     console.log(response);
// });