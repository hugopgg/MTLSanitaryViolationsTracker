// Validate login form inputs
function validateLoginForm() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    if (username.trim() === "") {
        document.getElementById("usernameError").innerText = "Le nom d'utilisateur est requis.";
        return false;
    }

    if (password.trim() === "") {
        document.getElementById("passwordError").innerText = "Le mot de passe est requis.";
        return false;
    }

    return true;
}

// Form submit
document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault(); 

    if (validateLoginForm()) {
        this.submit();
    }
});

