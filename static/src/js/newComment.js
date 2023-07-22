import axios from "axios";
import { getCookie } from "./getCookie";

const CommentForm = document.querySelector("#commentForm");
const csrftoken = getCookie('csrftoken');
const video_id = window.location.search.replace("?v=", "");



CommentForm.addEventListener("submit", (e) => {
    e.preventDefault();

    let commentBody = CommentForm.querySelector("#newComment");
    
    let  data = {
        commentBody: commentBody.value,
        video_id: video_id
    }

    console.log(commentBody);
    axios.post("new_comment/", data, {
        headers:{
            'X-CSRFToken': csrftoken
        }
    })
    .then((response) => {
        commentBody.value = "";
    })
    .catch((error) => {
        console.log(error);
    })
});