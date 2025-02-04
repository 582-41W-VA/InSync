window.onload = function() {
    const nameField = document.querySelector('#id_username');
    const loginPass = document.querySelector('#id_password');
    const password = document.querySelector('#id_password1');
    const confirmPassword = document.querySelector('#id_password2');
    const title = document.querySelector('#id_title');
    const content = document.querySelector('#id_content');
    const url = document.querySelector('#id_url')
    if (nameField) nameField.placeholder = "Enter your username";
    if (loginPass) loginPass.placeholder = "Enter your password";
    if (password) password.placeholder = "Enter your password";
    if (confirmPassword) confirmPassword.placeholder = " Confirm password";
    if (title) title.placeholder = "Post Title";
    if (content) content.placeholder = "Enter Content";
    if (url) url.placeholder = "Enter a Link Here";
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