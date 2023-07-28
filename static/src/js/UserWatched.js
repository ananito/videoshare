import videojs from 'video.js';
import axios from 'axios';

import { getCookie } from './getCookie';


const video_id = window.location.search.replace("?v=", "");
if (window.location.pathname === "/watch") {
    const player = videojs("my-video")

// when i use player.off() the video player icon does not work
let tries = 0;

player.on("play", () => {
    if (tries === 0) {
        let data = {
            video_id: video_id
        }
        axios.post(`update_views/${video_id}`, data, {
            headers: {
                'X-CSRFToken': getCookie("csrftoken")
            }
        })
        .catch((error) => {
            console.log(error);
        });
        
    }
    tries = 1;

});
}

