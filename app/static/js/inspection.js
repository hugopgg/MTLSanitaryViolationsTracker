// # ============================================
// # Auteur: Hugo Perreault Gravel 
// # ============================================


// Validate form inputs
function validateForm() {
    var etablissement = document.getElementById("etablissement").value;
    var adresse = document.getElementById("adresse").value;
    var ville = document.getElementById("ville").value;
    var dateDemande = document.getElementById("date_demande").value;
    var nomClient = document.getElementById("nom_client").value;
    var descriptionDemande = document.getElementById("description_demande").value;

    if (etablissement.trim() === "") {
        document.getElementById("etablissementError").innerText = "L'établissement est requis.";
        return false;
    }

    if (adresse.trim() === "") {
        document.getElementById("adresseError").innerText = "L'adresse est requise.";
        return false;
    }

    var adresseRegex = /^\d+\s[a-zA-Z\s']+$/; 
    if (!adresseRegex.test(adresse.trim())) {
        document.getElementById("adresseError").innerText = "Veuillez entrer une adresse valide.";
        return false;
    }

    if (ville.trim() === "") {
        document.getElementById("villeError").innerText = "La ville est requise.";
        return false;
    }

    if (dateDemande.trim() === "") {
        document.getElementById("dateDemandeError").innerText = "La date de demande est requise.";
        return false;
    }

    if (nomClient.trim() === "") {
        document.getElementById("nomClientError").innerText = "Votre nom est requis.";
        return false;
    }

    if (descriptionDemande.trim() === "") {
        document.getElementById("descriptionDemandeError").innerText = "Veuillez fournir une description de la demande.";
        return false;
    }

    return true;
}


// Send post request to '/api/demande_inspection' (create demande d'inspection)
function sendInspectionRequest() {
    var xhr = new XMLHttpRequest();
    var url = "/api/demande_inspection";

    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 201) {
                alert("Demande d'inspection envoyée avec succès !");
                window.location.href = "/";
            } else {
                alert("Une erreur s'est produite lors de l'envoi de la demande d'inspection.");
            }
        }
    };

    var formData = {
        etablissement: document.getElementById("etablissement").value,
        adresse: document.getElementById("adresse").value,
        ville: document.getElementById("ville").value,
        date_demande: document.getElementById("date_demande").value,
        nom_client: document.getElementById("nom_client").value,
        description_demande: document.getElementById("description_demande").value
    };

    xhr.send(JSON.stringify(formData));
}

// Form submit
document.getElementById("demandeInspectionForm").addEventListener("submit", function (event) {
    event.preventDefault();
    if (validateForm()) {
        sendInspectionRequest();
    }
});
