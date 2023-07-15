import axios from 'axios';

const uploadForm = document.getElementById('upload-form');
const progressBar = document.getElementById('progress-bar');
const message = document.querySelector("#upload-alert");


uploadForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData(uploadForm);

    // Get the CSRF token from the cookie
    const csrftoken = getCookie('csrftoken');

    axios.post('/upload/', formData, {
        headers: {
            'X-CSRFToken': csrftoken
        },
        onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            progressBar.style.width = percentCompleted + '%';
            progressBar.innerHTML = percentCompleted + "%";
        }
    }).then((response) => {
        message.querySelector("#message").innerHTML = response.data.message;
        message.className = "alert alert-dismissible fade show alert-success";
    }).catch((error) => {
        if (error.response) {
            message.querySelector("#message").innerHTML = error.response.data.message;
            message.className = "alert alert-dismissible fade show alert-danger";
        }
        // console.error(error);
    });
});

// Helper function to get the CSRF token from the cookie
function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}