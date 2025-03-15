// toggle_password.js

document.addEventListener("DOMContentLoaded", function () {
    const togglePassword = document.querySelector(".password-toggle");
    const passwordInput = document.querySelector("input[name='password']");

    togglePassword.addEventListener("click", function () {
        // Toggle the type attribute
        const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
        passwordInput.setAttribute("type", type);

        // Toggle the icon
        this.classList.toggle("fa-eye");
        this.classList.toggle("fa-eye-slash");
    });
});
