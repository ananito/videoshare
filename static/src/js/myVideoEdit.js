import axios from 'axios';
import * as bootstrap from 'bootstrap'
import { getCookie } from './getCookie';


if (window.location.pathname === "/user/videos/") {
    const csrftoken = getCookie('csrftoken');

    document.addEventListener("DOMContentLoaded", () => {
        let modal = document.querySelector("#editModal");
        const Bmodal = new bootstrap.Modal('#editModal');
        let videos = document.querySelectorAll(".video-container");

        videos.forEach(video => {
            let video_id = video.querySelector("#watchurl");
            video_id = video_id.search.replace("?v=", "");
            let editbtn = video.querySelector("#myVideoEdit");
            editbtn.addEventListener("click", () => {
                axios.get(`/getvideoinfo/${video_id}`)
                    .then(response => {
                        modal.querySelector("#title").value = response.data[0].fields.title;
                        modal.querySelector("#videoDescription").value = response.data[-0].fields.description;
                        modal.querySelector("#private").checked = response.data[-0].fields.private;
                    })

                Bmodal.show();
                let editform = modal.querySelector("#editform");


                editform.addEventListener("submit", (e) => {
                    e.preventDefault();
                    if (e.submitter.name == "delete") {
                        axios.delete(`/delete/${video_id}`, {
                            headers: {
                                'X-CSRFToken': csrftoken
                            }
                        })
                            .then((response) => {
                                Bmodal.hide();
                                video.className = "d-none";
                            })
                            .catch(error => {
                                console.log(error);
                            });
                    } else if (e.submitter.name == "update") {


                        let data = new FormData(e.target);
                        data.append("video_id", video_id);

                        axios.post("/user/videos/", data, {
                            headers: {
                                'X-CSRFToken': csrftoken
                            }
                        })
                            .then(response => {
                                video.querySelector(".card-title").innerHTML = editform.querySelector("#title").value;
                                Bmodal.hide();
                            })
                            .catch(error => {
                                console.log(error);
                            });
                    }

                });

            });
        });



    });
}