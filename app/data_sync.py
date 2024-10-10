# ============================================
# Auteur: Hugo Perreault Gravel 
# ============================================

import os
import csv
from database import Database
from email_sender import EmailSender
from data_utils import (
    get_data,
    convert_to_csv_data,
    get_current_violations,
    get_new_violations_list,
    apply_modifications_to_violations,
    apply_deletions_to_violations,
)

# ============================
# Data Synchronization
# ============================


# Sync data: retrieve new violations,
# update database, and send email if new violations found
def sync_data():
    violations_csv = "db/log/violations.csv"
    new_violations_csv = "db/log/new_violations.csv"
    violations_url = (
        "https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-"
        "5955efeb91a0/resource/7f939a08-be8a-45e1-b208-d8744dca8fc6/"
        "download/violations.csv"
    )
    violations_data = get_data(violations_url)

    # for test A3
    # with open("db/log/test.csv", "r") as file:
    #     violations_data = file.read()

    if violations_data:
        new_violations_list = []

        if os.path.exists(violations_csv):
            current_violations = get_current_violations(violations_csv)[1:]
            current_ids = set(violation[0] for violation in current_violations)

            new_violations = convert_to_csv_data(violations_data)[1:]
            new_violations_list = [
                violation
                for violation in new_violations
                if violation[0] not in current_ids
            ]

        # Update if new data found
        if new_violations_list:
            print("New data found...")
            try:
                with open(
                    new_violations_csv, "w", newline="", encoding="utf-8"
                ) as file:
                    writer = csv.writer(file)
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
                    writer.writerows(new_violations_list)
            except IOError as e:
                print("Error writing new violations to file:", e)

            # if data updated/deleted
            deleted_csv = "db/log/deleted_violations.csv"
            updated_csv = "db/log/updated_violations.csv"
            if os.path.exists(deleted_csv):
                apply_deletions_to_violations(violations_csv, deleted_csv)

            if os.path.exists(updated_csv):
                apply_modifications_to_violations(violations_csv, updated_csv)

            # redo the violations data with modifications
            with open("db/log/violations.csv", "r") as file:
                violations_data = file.read()

            # email
            violations_str = get_new_violations_list(new_violations_list)
            email_sender = EmailSender("app/config/email.yaml")
            email_body = "New violations found :\n" + violations_str
            email_sender.send_email("New violations found", email_body)

            db = Database()
            data_to_insert = convert_to_csv_data(violations_data)[1:]
            db.delete_all_violations()
            db.insert_all_violations(data_to_insert)
            db.disconnect()
            print("Database successfully updated")
        else:
            print("No new data found, database not updated")

    else:
        print("No data found, database not filled")


if __name__ == "__main__":
    sync_data()
