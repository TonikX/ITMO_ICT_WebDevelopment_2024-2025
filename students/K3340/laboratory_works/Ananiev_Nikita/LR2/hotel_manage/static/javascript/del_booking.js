let modal = document.getElementById("modal__del__book");
let del_btns = document.getElementsByClassName("btn__del__book");
let cancel_btn = document.getElementById("cancel__del");
let confirm_btn = document.getElementById("confirm__del");
let booking_id = "";
let csrftoken = getCookie('csrftoken');

Array.from(del_btns).forEach(function (del_btn) {
    del_btn.addEventListener('click', showModal)
})

function showModal() {
    modal.style.display = "block";
    booking_id = this.id;
}

cancel_btn.onclick = function closeModal() {
    modal.style.display = "none";
}

confirm_btn.onclick = function SendXMLHttp() {
    fetch("delete/" + booking_id, {
        method: "DELETE",
        headers:{
            "Content-Type":"application/json",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrftoken,
        },
    })
    modal.style.display = "none";
    document.getElementById("list__" + booking_id).remove();
}

function getCookie(name)
    {
      const regex = new RegExp(`(^| )${name}=([^;]+)`)
      const match = document.cookie.match(regex)
      if (match) {
        return match[2]
      }
   }