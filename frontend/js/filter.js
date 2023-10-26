const btn = document.querySelector('#btn');
btn.addEventListener('click', (event) => {
    let checkboxes = document.querySelectorAll('input[name="filter"]:checked');//беру все активные флажки

    // const lisTest = document.getElementsByClassName('author_name');
    // if(checkboxes){
    //     for(let liT of lisTest){
    //         if(liT.getAttribute('value')===checkboxes.item(0).getAttribute('value')){
    //             liT.style.display = '';
    //         }
    //         else{
    //             liT.style.display = 'none';
    //         }
    //     }
    // }

    const lis = document.querySelectorAll(`.search__panel__item`);//беру все значения книг
    let attributes = [];
    for(let v of checkboxes.values())
        attributes.push(v.getAttribute('value'));// формирую массив значений для поиска по авторам
    // for(let l of lis)
    //     console.log(l);
    if(checkboxes){
        for(let li of lis){
            // console.log(li)
            let l = li.querySelector('.author_name');// из книги беру класс автор
            // console.log(l)
            if(~attributes.indexOf(l.getAttribute('value'))){ //проверяю есть ли автор в активном фильтре
                li.style.display = '';
            }
            else{
                li.style.display = 'none'; // если его нет, то выключаю его видимость
            }
        }
    }
});