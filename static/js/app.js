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

const backButton = document.querySelector('.back-btn');
const mainHeader = document.querySelector('.main-header');
const searchHeader = document.querySelector('.search-header');
const searchbar = document.querySelector('.search-form');
const searchIcon = document.querySelector('.search-icon');

function replaceHeaders() {
    if (!searchbar) return;
    if (window.innerWidth <= 600) {
    searchbar.replaceWith(searchIcon);
    searchIcon.style.display = 'block'
    } else {
        if (searchHeader) {
            searchIcon.replaceWith(searchbar);
            searchIcon.style.display = 'none'
            showMainHeader()
        }
    }
}
  
function showMainHeader() {
    searchHeader.replaceWith(mainHeader);
    searchIcon.style.display = 'block'; 
}

function showSearchHeader() {
    mainHeader.replaceWith(searchHeader);
    searchIcon.style.display = 'none';  
    searchHeader.style.display = 'flex';
}

function responsiveHeader(){
    if (searchbar && searchIcon) {
        backButton.addEventListener('click', showMainHeader);
        searchIcon.addEventListener('click', showSearchHeader);
        window.addEventListener('load', replaceHeaders);
        window.addEventListener('resize', replaceHeaders);
    }
}
responsiveHeader();


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
            cancel()
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
                targetContainer.style.marginLeft = '30px';
                targetContainer.id = `replies-${parentCommentId}`;
                targetContainer.classList.add('comment-replies')
                parentCommentElement.appendChild(targetContainer);
            }
        } else {
            targetContainer = document.querySelector('#comments-list');
        }
        if (result.comment_html) {
            const newCommentElement = document.createElement('div'); 
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
            const closestFlash = event.target.closest('.flash-message')
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

function cancel(){
    const cancelBtn = document.querySelectorAll('.cancel-btn')
    cancelBtn.forEach(function(btn){
        btn.addEventListener('click', function(event){
            event.preventDefault
            const closestDetailEl = event.target.closest('details')
            if (closestDetailEl) closestDetailEl.removeAttribute('open');
        })
    })
}
cancel()

const currentPath = window.location.pathname;
const links = document.querySelectorAll('.profile-links a');
links.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
        link.classList.add('active');
    }
});

const fileInputs = document.querySelectorAll('#id_media, #id_profile_image');
const clearButtons = document.querySelectorAll('.clear-media-btn');
const mediaPreviewContainers = document.querySelectorAll('.media-preview');
const fileNamePreviews = document.querySelectorAll('.file-name-preview');
const mediaInputContainers = document.querySelectorAll('.media-input-container');

fileInputs.forEach((fileInput, index) => {
    const mediaPreview = mediaPreviewContainers[index];
    const fileNamePreview = fileNamePreviews[index];
    const mediaInputContainer = mediaInputContainers[index];
    const clearButton = clearButtons[index];

    if (mediaInputContainer) {
        if (fileInput) {
            fileInput.addEventListener('change', function(event) {
                handleFileSelect(event, fileInput, mediaPreview, fileNamePreview, clearButton);
            });
    
            mediaInputContainer.addEventListener('dragover', function(event) {
                handleDragOver(event, mediaInputContainer);
            });
    
            mediaInputContainer.addEventListener('dragleave', function(event) {
                handleDragLeave(event, mediaInputContainer);
            });
    
            mediaInputContainer.addEventListener('drop', function(event) {
                handleFileSelectFromDrop(event, fileInput, mediaPreview, fileNamePreview, clearButton, mediaInputContainer);
            });
        }
    }
    
    if (clearButton) {
        clearButton.addEventListener('click', function(event) {
            handleClear(event, fileInput, mediaPreview, fileNamePreview, clearButton);
        });
    }
});

function handleFileSelect(event, fileInput, mediaPreview, fileNamePreview, clearButton) {
    event.preventDefault();
    const file = event.target.files ? event.target.files[0] : event.dataTransfer.files[0];
    if (file) {
        displayPreview(file, mediaPreview, fileNamePreview);
        if (clearButton) clearButton.style.display = 'block';
    }
}

function handleDragOver(event, mediaInputContainer) {
    event.preventDefault();
    if (mediaInputContainer) {
        mediaInputContainer.classList.add('dragging');
    }
}

function handleDragLeave(event, mediaInputContainer) {
    event.preventDefault();
    if (mediaInputContainer) {
        mediaInputContainer.classList.remove('dragging');
    }
}

function handleFileSelectFromDrop(event, fileInput, mediaPreview, fileNamePreview, clearButton, mediaInputContainer) {
    event.preventDefault();
    if (mediaInputContainer) mediaInputContainer.classList.remove('dragging');
    const file = event.dataTransfer.files[0];

    if (file) {
        displayPreview(file, mediaPreview, fileNamePreview);
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;
    }
    const profileCheckbox = document.querySelector('#profile_image-clear_id');
    const mediaCheckbox = document.querySelector('#media-clear_id');
    if (profileCheckbox) profileCheckbox.checked = false;
    if (mediaCheckbox) mediaCheckbox.checked = false;
    if (clearButton) clearButton.style.display = 'block';
}

function displayPreview(file, mediaPreview, fileNamePreview) {
    mediaPreview.innerHTML = '';
    if (fileNamePreview) fileNamePreview.textContent = file.name;
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
    reader.readAsDataURL(file);
}

function handleClear(event, fileInput, mediaPreview, fileNamePreview, clearButton) {
    event.preventDefault();
    fileInput.value = '';
    mediaPreview.innerHTML = '';
    if (fileNamePreview) fileNamePreview.textContent = '';
    if (clearButton) clearButton.style.display = 'none';
    const profileCheckbox = document.querySelector('#profile_image-clear_id');
    const mediaCheckbox = document.querySelector('#media-clear_id');
    if (profileCheckbox) profileCheckbox.checked = true;
    if (mediaCheckbox) mediaCheckbox.checked = true;
}