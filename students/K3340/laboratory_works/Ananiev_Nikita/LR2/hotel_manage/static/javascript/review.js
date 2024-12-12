let modal = document.getElementById("modal__review");
let open_btn = document.getElementById("btn__review");
let close_btn = document.getElementsByClassName("modal__close")[0];

open_btn.onclick = function () {
    modal.style.display = "block";
}

close_btn.onclick = function () {
    modal.style.display = "none";
}