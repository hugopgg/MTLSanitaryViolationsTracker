// # ============================================
// # Auteur: Hugo Perreault Gravel 
// # ============================================



// Create table of infractions (between dates)
function createTable(response) {
    const violationCount = {};
    response.forEach(violation => {
        const etablissement = violation.etablissement;
        if (violationCount[etablissement]) {
            violationCount[etablissement]++;
        } else {
            violationCount[etablissement] = 1;
        }
    });

    const violationsSummary = Object.keys(violationCount).map(etablissement => {
        return {
            etablissement: etablissement,
            nombreInfractions: violationCount[etablissement],
            buisness_id: response.find(violation => violation.etablissement === etablissement).buisness_id
        };
    });


    // Table
    const table = document.createElement('table');
    table.setAttribute('class', 'table table-striped table-layout-fixed');
    // Header
    const headerRow = table.insertRow();
    const th1 = document.createElement('th');
    th1.setAttribute('scope', 'col')
    th1.textContent = 'Contrevenant';
    headerRow.appendChild(th1);
    const th2 = document.createElement('th');
    th2.setAttribute('scope', 'col')
    th2.textContent = 'Nombre d\'infractions';
    headerRow.appendChild(th2);
    const th3 = document.createElement('th');
    th3.setAttribute('scope', 'col')
    th3.textContent = 'Actions';
    headerRow.appendChild(th3);


    // Content
    violationsSummary.forEach(summary => {

        // Rows
        const row = table.insertRow();
        const cell1 = row.insertCell();
        cell1.textContent = summary.etablissement;
        const cell2 = row.insertCell();
        cell2.textContent = summary.nombreInfractions;
        const cell3 = row.insertCell();

        // Buttons
        const buttonContainer = document.createElement('div');
        buttonContainer.setAttribute('class', 'd-flex');
        const editButton = document.createElement('button');
        editButton.textContent = 'Modifier';
        editButton.setAttribute('class', 'btn btn-sm btn-secondary mx-2 index-btns-table');
        editButton.addEventListener('click', function () {
            const form = document.createElement('form');
            form.innerHTML = `
                <div class="mb-3 mt-3 text-center">
                    <label for="new-etablissement" class="form-label">Modifier le contrevenant:</label>
                    <input type="text" class="form-control" id="new-etablissement" placeholder="Entrez le nouveau contrevenant">
                </div>
                <div class="text-center">
                    <button type="submit" class="btn btn-primary index-btn-mod">Modifier</button>
                </div>
            `;
            cell3.appendChild(form);

            form.addEventListener('submit', function (event) {
                event.preventDefault();
                const newEtablissement = form.querySelector('#new-etablissement').value;
                const buisness_id = summary.buisness_id;
                updateEtablissement(buisness_id, newEtablissement);
                form.remove();
            });
        });
        buttonContainer.appendChild(editButton);
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Supprimer';
        deleteButton.setAttribute('class', 'btn btn-sm btn-secondary index-btn');
        deleteButton.addEventListener('click', function () {
            const buisness_id = summary.buisness_id;
            deleteViolationsByBuisnessId(buisness_id);
        });
        buttonContainer.appendChild(deleteButton);
        cell3.appendChild(buttonContainer);

    });

    return table;
}

// Update contrevenant
function updateEtablissement(buisnessId, newEtablissement) {
    const xhr = new XMLHttpRequest();
    const url = `/api/update_violations/${buisnessId}`;
    const data = {
        buisness_id: buisnessId,
        etablissement: newEtablissement
    };

    xhr.open('PUT', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function () {
        if (xhr.status === 200) {
            datesFormSubmit(new Event('submit'));
            alert("Établissement modifié avec succès !");
        } else {
            console.error("Erreur lors de la modification de l'établissement");
        }
    };

    xhr.onerror = function () {
        console.error('Erreur avec la requête de modification');
    };

    xhr.send(JSON.stringify(data));
}


// Delete violations of contrevenant
function deleteViolationsByBuisnessId(buisness_id) {
    const xhr = new XMLHttpRequest();
    const url = `/api/delete_violations/${buisness_id}`;

    xhr.open('DELETE', url, true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            datesFormSubmit(new Event('submit'));
            alert("Violations supprimées avec succès !");

        } else {
            console.error("Erreur lors de la suppression des violations");

        }
    };

    xhr.onerror = function () {
        console.error('Erreur avec la requête de suppression');
    };
    xhr.send();
}

// v.1 (première compréhension des specs)
// Create dropdown menu for search results (between dates) 
// function createDropdown(response) {
//     const dropdown = document.createElement('select');
//     dropdown.setAttribute('class', 'form-select mb-4');
//     dropdown.setAttribute('id', 'dropdown-results');

//     const etablissements = [];

//     // dropdown of etablissements
//     const defaultOption = document.createElement('option');
//     defaultOption.textContent = 'Liste des établissements';
//     defaultOption.value = '';
//     dropdown.appendChild(defaultOption);
//     response.forEach(violation => {
//         const etablissement = violation.etablissement;
//         const buisnessId = violation.buisness_id;
//         if (!etablissements.includes(etablissement)) {
//             etablissements.push(etablissement);
//             const option = document.createElement('option');
//             option.textContent = etablissement;
//             option.value = buisnessId;
//             dropdown.appendChild(option);
//         }
//     });

//     dropdown.addEventListener('change', function () {
//         const id = dropdown.value;
//         showViolationsByBuisnessId(id);

//     });

//     return dropdown;
// }


// Dates search results
function datesFormSubmit(event) {
    event.preventDefault();

    const startDate = document.getElementById('start_date').value;
    const endDate = document.getElementById('end_date').value;
    const url = `/api/violations?du=${startDate}&au=${endDate}`;
    const xhr = new XMLHttpRequest();

    xhr.open('GET', url, true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            const tableContainer = document.getElementById('table-container');
            const zeroElement = document.getElementById('zero-element');
            if (zeroElement) {
                zeroElement.parentNode.removeChild(zeroElement);
            }
            // const dropdown = createDropdown(response); (v.1)
            // tableContainer.appendChild(dropdown); (v.1)

            tableContainer.innerHTML = '';

            const title = document.createElement('h5');
            title.setAttribute('class', 'text-center');
            title.textContent = `Infractions du ${startDate} au ${endDate}:`;
            tableContainer.appendChild(title);
            const table = createTable(response);
            tableContainer.appendChild(table);
        } else if (xhr.status === 404) {
            console.error("Aucune violation trouvée")
            const divd = document.getElementById('drop-res');
            const divt = document.getElementById('table-container')
            divt.innerHTML = '';


            let zero = document.getElementById('zero-element');
            if (!zero) {
                zero = document.createElement('h4');
                zero.setAttribute('id', 'zero-element');
                zero.setAttribute('class', 'text-center');
                zero.textContent = 'Aucune infraction trouvée entre ces dates';
                divd.appendChild(zero);
            }
        }
    };

    xhr.onerror = function () {
        console.error('Erreur avec la requête')
    };
    xhr.send()
}


// Show all violations from buisness_id
function showViolationsByBuisnessId(buisnessId) {
    const xhr = new XMLHttpRequest();
    const url = `/api/violations/${buisnessId}`;

    xhr.open('GET', url, true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            const cardContainer = document.getElementById('table-container');
            cardContainer.innerHTML = '';

            response.forEach(violation => {
                const card = document.createElement('div');
                card.className = 'card article-card';
                card.innerHTML = `
                      <div class="card-header">
                          <h5 class="card-title">ID de la poursuite: ${violation.id_poursuite}</h5>
                      </div>
                      <div class="card-body">
                          <p class="card-text"><strong>Établissement:</strong> ${violation.etablissement}</p>
                          <p class="card-text"><strong>Catégorie:</strong> ${violation.categorie}</p>
                          <p class="card-text"><strong>Date:</strong> ${violation.date}</p>
                          <p class="card-text"><strong>Description:</strong> ${violation.description}</p>
                          <p class="card-text"><strong>Adresse:</strong> ${violation.adresse}</p>
                          <p class="card-text"><strong>Montant:</strong> ${violation.montant}</p>
                          <p class="card-text"><strong>Propriétaire:</strong> ${violation.proprietaire}</p>
                          <p class="card-text"><strong>Ville:</strong> ${violation.ville}</p>
                          <p class="card-text"><strong>Statut:</strong> ${violation.statut}</p>
                          <p class="card-text"><strong>Date de jugement:</strong> ${violation.date_jugement}</p>
                          <p class="card-text"><strong>Date de statut:</strong> ${violation.date_statut}</p>
                          
                      </div>
                  `;
                cardContainer.appendChild(card);
            });
        } else if (xhr.status === 404) {
            console.error("Aucune violation trouvée pour cet établissement");
        }
    };

    xhr.onerror = function () {
        console.error('Erreur avec la requête');
    };
    xhr.send();

}

// Etablissements (dropdown) change
function dropdownChange() {
    const dropdown = document.getElementById("list-etablissement");
    const buisness_id = dropdown.value;
    showViolationsByBuisnessId(buisness_id);
}

// Events Listeners
document.getElementById("search-form-dates").addEventListener("submit", datesFormSubmit);
document.getElementById("list-etablissement").addEventListener("change", dropdownChange);