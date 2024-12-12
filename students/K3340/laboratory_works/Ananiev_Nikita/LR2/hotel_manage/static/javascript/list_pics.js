let next_btn = document.getElementById("next__pic");
let prev_btn = document.getElementById("prev__pic");
let pics = document.getElementsByClassName("list__pic");
let shown_count = 2;

let pic_index = shown_count - 1;
let max_index = pics.length - 1;

window.onload = function () {
    prev_btn.disabled = true;
    if (max_index < shown_count)
        next_btn.disabled = true;
    pic_index = shown_count - 1;
    for (let i = 0; i < shown_count; i++)
        pics[i].style.display = "block";
}

next_btn.onclick = function () {
    pic_index++;
    pics[pic_index - shown_count].style.display = "none";
    pics[pic_index].style.display = "block";
    if (prev_btn.disabled)
        prev_btn.disabled = false;
    if (pic_index === max_index)
        next_btn.disabled = true;
}

prev_btn.onclick = function () {
    pic_index--;
    pics[pic_index + 1].style.display = "none";
    pics[pic_index - shown_count + 1].style.display = "block";
    if (next_btn.disabled)
        next_btn.disabled = false;
    if (pic_index === shown_count - 1)
        prev_btn.disabled = true;
}