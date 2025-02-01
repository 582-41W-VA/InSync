window.onload = function() {
    const nameField = document.querySelector('#id_username');
    const emailField = document.querySelector('#id_password');
    if (nameField) nameField.placeholder = "Enter your username";
    if (emailField) emailField.placeholder = "Enter your password";
};