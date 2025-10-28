/*
* Autor: Hugo Martín Alonso
* Fecha: 25-09-2025
* Descripción: script para dinamizar la página de login.
*/


//const enableLog = () => document.getElementById("login").disabled = false;
//const disableLog = () => document.getElementById("login").disabled = true;

const buttonLogin = document.getElementById("login");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");

usernameInput.addEventListener("input", () => {
    console.log("Usuario:", usernameInput.value);
});

buttonLogin.addEventListener("click", () => {
    const username = usernameInput.value;
    const password = passwordInput.value;
});


/* TODO acabar la función
function isUserValid(username) {
    
    if(isNullOrEmpty(username)) {
        return false;
    }
    else if(username.length < 3 || username.length > 20) {
        return false;
    }
    else {
        return true;
    }
}*/