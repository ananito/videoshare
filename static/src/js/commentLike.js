import axios from "axios";
import { getCookie } from "./getCookie";

const csrftoken = getCookie("csrftoken");
const video_id = window.location.search.replace("?v=", "");




let like_btns = document.querySelectorAll(".commentlikes");


like_btns.forEach(btn => {
    btn.addEventListener("click", () => {

        let data = {
            comment_id: btn.dataset.id,
            video_id: video_id
        }


        axios.post("like_comment/", data, {
            headers:{
                "X-CSRFToken": csrftoken,
            }
        })

        .then((response) => {
            btn.querySelector("span").innerHTML = response.data.data.total;
        })
        .catch((error) => {
            console.log(error);
        })
    });
});