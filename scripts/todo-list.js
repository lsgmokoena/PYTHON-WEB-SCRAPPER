const todoList = [];

function addTodo()
{
    const inputElement = document.querySelector('.js-input-name');
    const name = inputElement.value;
    todoList.push(name);
    console.log(todoList);
}

function addTodo2(){
    const inputElement = document.querySelector('.js-input-name');
    const name = inputElement.value;
    todoList.push(name);
    console.log(todoList);

    let todoListHTML = '';
    let htmlText ='';

    inputElement.value = '';

    for(let i = 0; i < todoList.length; i++){
        let todo = todoList[i];
        htmlText = '<p>'+ todo +'</p>';
        todoListHTML += htmlText;
        
        document.querySelector('.js-todoList').innerHTML = todoListHTML;
    }


}