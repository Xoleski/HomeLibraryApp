const loginForm = document.getElementById("login");

loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const response = await api.auth.login({email: this.email.value, password: this.password.value});
    if (response !== undefined) {
        localStorage.setItem("accessToken", response.data.access_token);
        localStorage.setItem("refreshToken", response.data.refresh_token);
        localStorage.setItem("tokenType", response.data.token_type);
        window.location.href = "/"
    }
})


document.addEventListener("DOMContentLoaded", async (e) => {
    const queryParams = window.location.search;
    if (queryParams !== "") {
        const response = await api.auth.google(queryParams);
        if (response !== undefined) {
            localStorage.setItem("accessToken", response.data.access_token);
            localStorage.setItem("refreshToken", response.data.refresh_token);
            localStorage.setItem("tokenType", response.data.token_type);
            window.location.href = "/"
        }
    }
})
