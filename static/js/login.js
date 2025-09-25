
//const enableLog = () => document.getElementById("login").disabled = false;
//const disableLog = () => document.getElementById("login").disabled = true;

const buttonLogin = document.getElementById("login");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");

usernameInput.addEventListener("input", () => {
    console.log("Usuario:", usernameInput.value);
});

buttonLogin.addEventListener("click", () => {
    username = usernameInput.value;
    password = passwordInput.value;
}
    

/*
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