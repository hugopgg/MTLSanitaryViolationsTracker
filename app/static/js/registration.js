// Validate form inputs
function validateForm() {
    var nom = document.getElementById("nom").value;
    var prenom = document.getElementById("prenom").value;
    var username = document.getElementById("username").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;


    if (nom.trim() === "") {
        document.getElementById("nomError").innerText = "Le nom est requis.";
        return false;
    }

    if (prenom.trim() === "") {
        document.getElementById("prenomError").innerText = "Le prénom est requis.";
        return false;
    }

    if (username.trim() === "") {
        document.getElementById("usernameError").innerText = "Le nom d'utilisateur est requis.";
        return false;
    }

    if (email.trim() === "") {
        document.getElementById("emailError").innerText = "L'email est requis.";
        return false;
    }

    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.trim())) {
        document.getElementById("emailError").innerText = "Veuillez entrer une adresse email valide.";
        return false;
    }

    if (password.trim() === "") {
        document.getElementById("passwordError").innerText = "Le mot de passe est requis.";
        return false;
    }

    if (password.trim().length < 8) {
        document.getElementById("passwordError").innerText = "Le mot de passe doit contenir au moins 8 caractères.";
        return false;
    }
    return true;
}

// Send post request to '/api/create_user' (create new user)
function sendUserCreationRequest() {
    var xhr = new XMLHttpRequest();
    var url = "/api/create_user";

    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 201) {
                alert("Utilisateur créé avec succès !");
                window.location.href = "/";
            } else {
                alert("Une erreur s'est produite lors de la création de l'utilisateur.");
            }
        }
    };

    var formData = {
        nom: document.getElementById("nom").value,
        prenom: document.getElementById("prenom").value,
        username: document.getElementById("username").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
        etablissements: document.getElementById("etablissements").value.split(",").map(item => item.trim())
    };

    xhr.send(JSON.stringify(formData));
}

// Form submit
document.getElementById("inscriptionForm").addEventListener("submit", function (event) {
    event.preventDefault();
    if (validateForm()) {
        sendUserCreationRequest();
    }
});
