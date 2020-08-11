
window.onload=load_func;
let login_word=document.getElementById('login_word');
let register_word=document.getElementById('register_word');
document.getElementById("products").addEventListener('mouseover',products_display);
document.getElementById("brands").addEventListener('mouseover',brands_display);
document.getElementById("user-profile").addEventListener('mouseover',profile_display);

document.getElementById("products").addEventListener('mouseout',lost_focus);
document.getElementById("brands").addEventListener('mouseout',lost_focus);
document.getElementById("user-profile").addEventListener('mouseout',lost_focus);

if(login_word!=null){
    login_word.addEventListener('click',display_login_form);
}

if(register_word!=null){
    register_word.addEventListener('click',display_register_form);
}

function load_func(){
    display_login_form();
    if(document.getElementById("advertisements")!=null){
        advertisement();
    }
    if(document.getElementsByClassName("messages")!=null){
        message_ele=document.getElementsByClassName("messages");
    }
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
    document.getElementById("products").style.backgroundColor = "#353535";
    document.getElementById("products_display_base").style.visibility = "visible";
}

function brands_display(){
    document.getElementById("brands").style.backgroundColor = "#353535";
    document.getElementById("brands_display_base").style.visibility = "visible";
}

function profile_display(){
    document.getElementById("user-profile").style.backgroundColor = "#353535";
    if(document.getElementById("profile_display_base")!=null){
        document.getElementById("profile_display_base").style.visibility = "visible";
    }
}

function lost_focus() {
    document.getElementById("products").style.backgroundColor = "";
    document.getElementById("brands").style.backgroundColor = "";
    document.getElementById("user-profile").style.backgroundColor = "";
    document.getElementById("products_display_base").style.visibility = "hidden";
    document.getElementById("brands_display_base").style.visibility = "hidden";
    if(document.getElementById("profile_display_base")!=null){
        document.getElementById("profile_display_base").style.visibility = "hidden";
    }
}

function advertisement() {
    var randomColor1 = '#'+Math.floor(Math.random()*16777215).toString(16);
    var randomColor2 = '#'+Math.floor(Math.random()*16777215).toString(16);
    document.getElementById("advertisements").style.backgroundImage = "linear-gradient(to right bottom, "+randomColor1+", "+randomColor2+")";
    setTimeout(function(){ advertisement() }, 3000);
}

let message_ele;

setTimeout(function(){
    for (let i = 0; i < message_ele.length; i++) {
        message_ele[i].style.display = "none";
    }
}, 3000);


