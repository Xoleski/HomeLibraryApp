const registerForm = document.getElementById("register");

registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const response = await api.auth.register(
        {email: this.email.value, password: this.password.value, confirm_password: this.confirm_password.value}
    );
    if (response !== undefined) {
        window.location.href = "/login"
    }
})