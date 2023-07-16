import axios from 'axios';
import { getCookie } from './getCookie';


window.addEventListener("DOMContentLoaded", () => {
    const urlpath = window.location.pathname;
    if (String(urlpath) === "/watch") {
        like_dislike()
    }
});

function like_dislike() {
    const like_btn = document.querySelector("#like_btn");
    const dislike_btn = document.querySelector("#dislike_btn");
    const video_id = window.location.search.replace("?v=", "");

    like_btn.addEventListener("click", () => {
        // console.log(like_btn.dataset.uniqueId);
        let  data = {
            video_id: video_id,
            unique_id: like_btn.dataset.uniqueId
        }
        send_request("like", data);
    });

    dislike_btn.addEventListener("click", () => {
        let  data = {
            video_id: video_id,
            unique_id: like_btn.dataset.uniqueId
        }
        send_request("dislike", data);
    });

    function send_request(type,data) {
        axios.post(`like_dislike/${type}`, data,
            {
                headers: {
                    'X-CSRFToken': getCookie("csrftoken")
                }
            }).then((response) => {
                like_btn.querySelector("span").innerHTML = response.data.message.like;
                dislike_btn.querySelector("span").innerHTML = response.data.message.dislike;
            }).catch((error) => {
                console.log(error);
            });
    }

}