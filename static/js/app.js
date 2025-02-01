window.onload = function() {
    const nameField = document.querySelector('#id_username');
    const emailField = document.querySelector('#id_password');
    if (nameField) nameField.placeholder = "Enter your username";
    if (emailField) emailField.placeholder = "Enter your password";
};

const menu = document.querySelector('.menu-icon')
menu.addEventListener('click', headerToggle)

function headerToggle() {
    let header = document.querySelector("header");
    header.classList.toggle("responsive");
    document.body.classList.toggle("header-open");
}

function headerClose() {
    let header = document.querySelector("header");
    if (window.innerWidth > 700) {
      header.classList.remove("responsive");
      document.body.classList.remove("header-open");
    }
}
window.addEventListener('load', headerClose);
window.addEventListener('resize', headerClose);