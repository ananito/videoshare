import "axios.min.js"

window.addEventListener("DOMContentLoaded", () => {
    const urlpath = window.location.pathname;
    if (String(urlpath) === "/watch") {
        like()
    }
});

function like() {
    const like_btn = document.querySelector("#like_btn");
    console.log(like_btn);
    axios.get;
}