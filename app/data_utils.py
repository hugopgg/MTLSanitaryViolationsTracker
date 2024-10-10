# ============================================
# Auteur: Hugo Perreault Gravel 
# ============================================

from io import StringIO
import csv
import os
import requests

# ==================================================
# Utility Functions for Data Management
# ==================================================


# Get data from url
def get_data(url):
    print("Retrieving data from source...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        print("Error retrieving data:", e)
        return None


# Convert data to csv data
def convert_to_csv_data(data):
    csv_data = StringIO(data)
    csv_reader = csv.reader(csv_data, delimiter=",")
    return list(csv_reader)


# Get current violations (stored in csv file)
def get_current_violations(csv_file):
    current_violations = []
    try:
        with open(csv_file, "r", newline="", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                current_violations.append(row)
    except IOError as e:
        print("Error reading the violations file:", e)
    return current_violations


# Format new violations list for email
def get_new_violations_list(new_violations_list):
    violations_str = ""
    for violation in new_violations_list:
        violations_str += ", ".join(violation) + "\n"
    return violations_str


# Write deleted violations to csv
def write_violations_to_csv(violations, file):
    try:
        file_exists = os.path.exists(file)
        with open(file, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(
                    [
                        "id_poursuite",
                        "buisness_id",
                        "date",
                        "description",
                        "adresse",
                        "date_jugement",
                        "etablissement",
                        "montant",
                        "proprietaire",
                        "ville",
                        "statut",
                        "date_statut",
                        "categorie",
                    ]
                )
            for violation in violations:
                writer.writerow(
                    [
                        violation.id_poursuite,
                        violation.buisness_id,
                        violation.date,
                        violation.description,
                        violation.adresse,
                        violation.date_jugement,
                        violation.etablissement,
                        violation.montant,
                        violation.proprietaire,
                        violation.ville,
                        violation.statut,
                        violation.date_statut,
                        violation.categorie,
                    ]
                )
    except IOError as e:
        print("Error writing deleted violations to file:", e)


# Apply deletions to violations file
def apply_deletions_to_violations(violations_csv, deleted_csv):
    if os.path.exists(deleted_csv):
        with open(deleted_csv, "r") as delete_file:
            reader = csv.reader(delete_file)
            next(reader)
            for row in reader:
                delete_violation(violations_csv, row[0])


# Delete violations in file
def delete_violation(violations_csv, id_poursuite):
    with open(violations_csv, "r") as file:
        lines = file.readlines()

    with open(violations_csv, "w") as file:
        for line in lines:
            if not line.startswith(id_poursuite):
                file.write(line)


# Apply modifications to violations file
def apply_modifications_to_violations(violations_csv, updated_csv):
    if os.path.exists(updated_csv):
        with open(updated_csv, "r") as modify_file:
            reader = csv.reader(modify_file)
            next(reader)
            for row in reader:
                modify_violation(violations_csv, row)


# Update violations in file
def modify_violation(violations_csv, new_violation_data):
    with open(violations_csv, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        lines = list(reader)

    for i, line in enumerate(lines):
        if line[0] == new_violation_data[0]:
            lines[i] = new_violation_data
            break

    with open(violations_csv, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(lines)
