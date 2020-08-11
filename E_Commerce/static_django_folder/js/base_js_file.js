
window.onload=display_login_form;
let login_word=document.getElementById('login_word');
let register_word=document.getElementById('register_word');
document.getElementById("products").addEventListener('blur',products_display)

if(login_word!=null){
    login_word.addEventListener('click',display_login_form);
}

if(register_word!=null){
    register_word.addEventListener('click',display_register_form);
}

function display_login_form(){

    let temp1=document.getElementById("login_word");

    let temp2=document.getElementById("register_word");

    if(temp1!=null&&temp2!=null){
        temp1.style.boxShadow="";



        temp2.style.boxShadow="5px 5px 10px #8caab8 inset";

        let myElements = document.querySelectorAll(".register-form");

        for (let i = 0; i < myElements.length; i++) {
            myElements[i].style.display = "none";
        }

        myElements = document.querySelectorAll(".login-form");

        for (let i = 0; i < myElements.length; i++) {
            myElements[i].style.display = "";
        }
    }
}

function display_register_form(){

    let temp1=document.getElementById("login_word");

    temp1.style.boxShadow="5px 5px 10px #8caab8 inset";

    let temp2=document.getElementById("register_word");

    temp2.style.boxShadow="";

    let myElements = document.querySelectorAll(".login-form");

    for (let i = 0; i < myElements.length; i++) {
        myElements[i].style.display = "none";
    }

    myElements = document.querySelectorAll(".register-form");

    for (let i = 0; i < myElements.length; i++) {
        myElements[i].style.display = "";
    }
}

function products_display(){
    document.getElementById("products_display_base").style.display="";
}
