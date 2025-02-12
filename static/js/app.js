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
            createComment(result, form)
            editComment(result)
            deleteComment(result)
            const button = form.querySelector('button');
            handleInteractions(result, button, form)
            closeDetails();
            iconState();
            handleFlashMessage(result, button)
        }
    } catch (error) {
        console.error('Error submitting form:', error);
    }
}

function createComment(result, form) {
    if (result.action === 'create') {
        form.reset();
        const parentCommentId = form.querySelector('[name=parent_comment_id]')?.value;
        let targetContainer;
        if (parentCommentId) {
            targetContainer = document.querySelector(`#replies-${parentCommentId}`);
            if (!targetContainer) {
                const parentCommentElement = document.querySelector(`#comment-${parentCommentId}`);
                targetContainer = document.createElement('ul');
                targetContainer.style.marginLeft = '65px';
                targetContainer.id = `replies-${parentCommentId}`;
                targetContainer.classList.add('comment-replies')
                parentCommentElement.appendChild(targetContainer);
            }
        } else {
            targetContainer = document.querySelector('#comments-list');
        }
        if (result.comment_html) {
            const newCommentElement = document.createElement('li');
            newCommentElement.classList.add('ea-comment')
            newCommentElement.id = `comment-${result.comment_id}`; 
            newCommentElement.innerHTML = result.comment_html;
            targetContainer.appendChild(newCommentElement);
        }
    }
}

function editComment(result){
    if (result.action === 'edit') {
        const oldCommentElement = document.querySelector(`#comment-${result.comment_id}`);
        if (oldCommentElement) oldCommentElement.innerHTML = result.comment_html;
    } 
}

function deleteComment(result){
    if (result.action === 'delete'){
        const commentElementToDelete = document.querySelector(`#comment-${result.comment_id}`);
        if (commentElementToDelete) commentElementToDelete.remove();
    }
}

function toggleLikes(result, button, form){
    if (result.action === 'upvote') {
        displayMessage(form, 'flash', result.message);
        const icon = button.querySelector('i');
        let countEl = button.querySelector('.likes-count');
        if (!countEl) {
            countEl = document.createElement('p');
            countEl.classList.add('likes-count');
            button.appendChild(countEl);
        }
        icon.className = result.is_added 
            ? icon.className.replace('fa-regular', 'fa-solid') 
            : icon.className.replace('fa-solid', 'fa-regular') 
                
        countEl.textContent = result.upvotes;
    }   
}

function toggleSave(result, form, button){
     if (result.action === 'save') {
        displayMessage(form, 'flash', result.message);
        const icon = button.querySelector('i')
        icon.className = result.is_added
            ?   icon.className.replace('fa-regular', 'fa-solid')
            :   icon.className.replace('fa-solid', 'fa-regular');
    }
}

function handleFlag(button, result){
    if (result.action === 'flag') {
        const formContainer = button.closest('.action-form')
        if (formContainer) formContainer.innerHTML = result.message
    }
}

function handleInteractions(result, button, form){
    if (result) {
        toggleLikes(result, button, form)
        toggleSave(result, form, button)
        handleFlag(button, result)
    }
}

function displayMessage(form, flash, message) {
    form.style.position = 'relative';
    const messageP = document.createElement("span");
    messageP.classList.add(flash);
    messageP.textContent = message
    form.appendChild(messageP);
    requestAnimationFrame(() => {
        messageP.classList.add('shows');
    });
    setTimeout(() => {
        messageP.classList.remove('shows');
        messageP.classList.add('hide');
        setTimeout(() => {
            messageP.remove();
        }, 400); 
    }, 1300);
}

function handleFlashMessage(result){
    if(result.flash_message_html){
        document.querySelector('.target-container').innerHTML = result.flash_message_html;
        closeFlashMessages()
    }
}

function iconState(){
    const detailsElements = document.querySelectorAll('details');
    detailsElements.forEach(function(detailsElement) {
        const icon = detailsElement.querySelector('summary i');
        detailsElement.addEventListener('toggle', function() {
            icon.className = detailsElement.open
            ? icon.className.replace('fa-regular', 'fa-solid')
            : icon.className.replace('fa-solid', 'fa-regular');
        });
    });
}
iconState()

function closeFlashMessages(){
    const closeFlash = document.querySelectorAll('.flash-message i')
    closeFlash.forEach(function(close) {
        close.addEventListener('click', function(event){
            console.log('hi')
            const closestFlash = event.target.closest('.flash-message')
            console.log(closeFlash, closestFlash)
            if(closestFlash) closestFlash.remove()
        })
    })
}
closeFlashMessages()

function closeDetails() {
    const detailsElement = document.querySelectorAll('#replyDetails');
    detailsElement.forEach(function(el) {
        if(el) el.removeAttribute('open');
    });
}

const currentPath = window.location.pathname;
const links = document.querySelectorAll('.profile-links a');
links.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
        link.classList.add('active');
    }
});

const fileInput = document.querySelector('#id_media');
const mediaPreview = document.querySelector('.media-preview');
const fileNamePreview = document.querySelector('.file-name-preview');
const mediaInputContainer = document.querySelector('.media-input-container');
const clearButton = document.getElementById('clear-media');

if (fileInput) {
    fileInput.addEventListener('change', handleFileSelect);
    mediaInputContainer.addEventListener('dragover', handleDragOver);
    mediaInputContainer.addEventListener('dragleave', handleDragLeave);
    mediaInputContainer.addEventListener('drop', handleFileSelectFromDrop);
}

function handleFileSelect(event) {
    event.preventDefault();
    const file = event.target.files ? event.target.files[0] : event.dataTransfer.files[0];
    if (file) {
        displayPreview(file);
    }
}

function handleDragOver(event) {
    event.preventDefault();
    mediaInputContainer.classList.add('dragging');
}

function handleDragLeave(event) {
    event.preventDefault();
    mediaInputContainer.classList.remove('dragging');
}

function handleFileSelectFromDrop(event) {
    event.preventDefault();
    mediaInputContainer.classList.remove('dragging');
    const file = event.dataTransfer.files[0];

    if (file) {
        displayPreview(file);
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files; 
    }

    const checkbox = document.querySelector('#media-clear_id');
    if (checkbox) {
        checkbox.checked = false;
    }
}

function displayPreview(file) {
    mediaPreview.innerHTML = '';
    fileNamePreview.textContent = file.name;
    const reader = new FileReader();

    reader.onload = function (e) {
        const mediaUrl = e.target.result;

        if (file.type.startsWith('image')) {
            const img = document.createElement('img');
            img.src = mediaUrl;
            mediaPreview.appendChild(img);
        } else if (file.type.startsWith('video')) {
            const video = document.createElement('video');
            video.src = mediaUrl;
            video.controls = true;
            mediaPreview.appendChild(video);
        }
    };
    clearButton.style.display = 'block';
    reader.readAsDataURL(file);
}

if (clearButton) {
    clearButton.addEventListener('click', function(event) {
    event.preventDefault()
    fileInput.value = '';
    mediaPreview.innerHTML = '';
    fileNamePreview.textContent = '';
    clearButton.style.display = 'none';

    const checkbox = document.querySelector('#media-clear_id');
    if (checkbox) {
        checkbox.checked = true;
    }
});
}
