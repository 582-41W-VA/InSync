window.onload = function() {
    const nameField = document.querySelector('#id_username');
    const loginPass = document.querySelector('#id_password');
    const password = document.querySelector('#id_password1');
    const confirmPassword = document.querySelector('#id_password2');
    if (nameField) nameField.placeholder = "Enter your username";
    if (loginPass) loginPass.placeholder = "Enter your password";
    if (password) password.placeholder = "Enter your password";
    if (confirmPassword) confirmPassword.placeholder = " Confirm password";
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
    if (window.innerWidth > 900) {
      header.classList.remove("responsive");
      document.body.classList.remove("header-open");
    }
}
window.addEventListener('load', headerClose);
window.addEventListener('resize', headerClose);
function main() {
    document.body.addEventListener('submit', function(event) {
        if (event.target && event.target.matches('.action-form')) {
            handleFormSubmit(event);  
        }
    });
}
main();

async function handleFormSubmit(event) {
    event.preventDefault();
    const form = event.target.closest('form'); 
    if (!form) return;
    const formData = new FormData(form);
    const formMethod = form.method;
    const actionUrl = form.action;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    await sendForm(actionUrl, formMethod, form, formData, csrfToken);
}

async function sendForm(actionUrl, formMethod, form, formData, csrfToken) {
    const options = {
        method: formMethod,
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken
        }
    };
    await handleRequest(actionUrl, options, form);
}
    
async function handleRequest(actionUrl, options, form){
    try {
        const response = await fetch(actionUrl, options)
        if (!response.ok) {
            const result = await response.json();
            if (response.status === 401 && result.redirect) {
                window.location.href = result.redirect;
                return;
            }
        }

        const result = await response.json();
        if (result) {
            const button = form.querySelector('button');
            handleInteractions(result, button)
        }
    } catch (error) {
        console.error('Error submitting form:', error);
    }
}

function handleInteractions(result, button){
    if (result) {
        if (result.action === 'upvote') {
            button.innerHTML = result.is_added
                ? `<i class="fa-solid fa-heart"></i>
                <p class="likes-count">Likes: ${result.upvotes}</p>`
                : `<i class="fa-regular fa-heart"></i>
                <p class="likes-count">Likes: ${result.upvotes}</p>`;
        }   

        if (result.action === 'flag') {
            const formContainer = button.closest('.action-form')
            if (formContainer) formContainer.innerHTML = result.message
        }

        if (result.action === 'save') {
            button.innerHTML = result.is_added
                ? '<i class="fa-solid fa-bookmark"></i>'
                : '<i class="fa-regular fa-bookmark"></i>';
        }
    }
}

const detailsElements = document.querySelectorAll('.interaction details');
detailsElements.forEach(function(detailsElement) {
    const icon = detailsElement.querySelector('summary i');
    detailsElement.addEventListener('toggle', function() {
        if (detailsElement.open) {
            icon.classList.remove('fa-regular');
            icon.classList.add('fa-solid');
        } else {
            icon.classList.remove('fa-solid');
            icon.classList.add('fa-regular');
        }
    });
});


const closeFlash = document.querySelectorAll('.flash-message i')
closeFlash.forEach(function(close) {
    close.addEventListener('click', function(event){
        const closestFlash = event.target.closest('.flash-message')
        if(closestFlash) closestFlash.remove()
    })
})
