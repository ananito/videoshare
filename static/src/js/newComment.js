import axios from "axios";
import { getCookie } from "./getCookie";
if (window.location.pathname === "/watch") {

const CommentForm = document.querySelector("#commentForm");
const csrftoken = getCookie("csrftoken");
const video_id = window.location.search.replace("?v=", "");

CommentForm.addEventListener("submit", (e) => {
  e.preventDefault();

  let commentBody = CommentForm.querySelector("#newComment");

  let commentlists = document.querySelector(".comment-lists");

  let data = {
    commentBody: commentBody.value,
    video_id: video_id,
  };

  console.log(commentBody);
  axios
    .post("new_comment/", data, {
      headers: {
        "X-CSRFToken": csrftoken,
      },
    })
    .then((response) => {
        console.log(response);
      commentBody.value = "";

      let newcomment = document.createElement("div");
      newcomment.className = "card-body border-top";
      newcomment.innerHTML = `<div class="row">
                                        <div class="col">
                                        <h5 class="card-title"><a class="link link-underline  link-underline-opacity-0" href="" data-id="${response.data.data.id}">${response.data.data.username}</a></h5>
                                        </div>
                                    </div>
                                    <!-- Comment Date -->
                                    <p class="small">${response.data.data.created_at} </p>
                                    <!-- Comment Content -->
                                    <p id="comment-body">${response.data.data.body} </p>

                                    <!-- Like count -->
                                    <div class="d-flex commentlikes" data-id="${response.data.data.id}">
                                        Likes <span class="ms-1">${response.data.data.likes}</span>
                                    </div>
                                `;
        commentlists.prepend(newcomment);

    //   console.log(response.data.data);
    })
    .catch((error) => {
        if (error.response.data.error) {
            let alert_message = document.querySelector("#comment-error");
            alert_message.querySelector(".alert-message").innerHTML = error.response.data.error;
            alert_message.classList.remove("d-none");
            console.log(error.response.data.error);
            alert_message.querySelector(".btn-close").addEventListener("click", ()=> {
                alert_message.classList.add("d-none");
            });
        }
    });
});
}
