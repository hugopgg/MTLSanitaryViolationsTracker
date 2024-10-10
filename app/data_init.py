# ============================================
# Auteur: Hugo Perreault Gravel 
# ============================================

import os
from database import Database
from data_utils import get_data, convert_to_csv_data

# ===========================
# Data Initialization
# ===========================


# Get data from URL and fill the database
def initialize_data():
    violations_url = (
        "https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-"
        "5955efeb91a0/resource/7f939a08-be8a-45e1-b208-d8744dca8fc6/"
        "download/violations.csv"
    )

    violations_data = get_data(violations_url)
    violations_csv = "db/log/violations.csv"

    if violations_data:
        if not os.path.exists(violations_csv):
            try:
                with open(violations_csv, "w") as file:
                    file.write(violations_data)
                db = Database()
                data_to_insert = convert_to_csv_data(violations_data)[1:]
                db.insert_all_violations(data_to_insert)
                db.disconnect()
                print("Database successfully filled")
            except IOError as e:
                print("Error writing to file:", e)
        else:
            print("Database already filled")
    else:
        print("No data found, database not filled")


if __name__ == "__main__":
    initialize_data()
