# ============================================
# Auteur: Hugo Perreault Gravel 
# ============================================

from flask import Flask, render_template
from flask import g, request, jsonify, session
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import subprocess
from functools import wraps
from datetime import datetime, timedelta
import secrets
import csv
from io import StringIO
import hashlib
import uuid

from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

from flask import jsonify
from flask_json_schema import JsonSchema
from flask_json_schema import JsonValidationError

from database import Database
from data_utils import write_violations_to_csv
from error_messages import get_error_message

from models.demandeInspection import DemandeInspection
from models.user import User
from schemas import insert_demande_inspection_schema
from schemas import update_contrevenant_schema
from schemas import insert_user_schema

from flask_httpauth import HTTPBasicAuth


# ===========
# APP
# ===========

# app settings
app = Flask(__name__, static_url_path="/static", static_folder="static")
app.config["SECRET_KEY"] = secrets.token_hex(16)
schema = JsonSchema(app)
basic_auth = HTTPBasicAuth()

# update violations sync every day at midnight (hour=0)
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=lambda: subprocess.run(["python", "app/data_sync.py"]),
    trigger=CronTrigger(hour=0),
)

# scheduler.add_job(
#     func=lambda: subprocess.run(["python", "app/data_sync.py"]),
#     trigger="date",
#     run_date=datetime.now() + timedelta(seconds=25)
# )  # test

scheduler.start()


# ============================
# General Functions
# ============================


# Get the database
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        g._database = Database()
    return g._database


# Disconnect the database
@app.teardown_appcontext
def disconnection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.disconnect()


# 404 Error Handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


# 405 Error Handling
@app.errorhandler(405)
def method_not_allowed(error):
    return render_template("405.html"), 405


# JSON validation error handling
@app.errorhandler(JsonValidationError)
def validation_error(e):
    errors = [validation_error.message for validation_error in e.errors]
    return jsonify({"error": e.message, "errors": errors}), 400


# =====================
# Basic authentication
# =====================

# Pour fin de correction: username=prof, password=secret1234
@basic_auth.verify_password
def verify_password(username, password):
    db = get_db()
    user = db.get_login_info(username)
    if user:
        salt = user[0]
        h_pw = hashlib.sha512(str(password + salt).encode("utf-8")).hexdigest()
        if h_pw == user[1]:
            return True
    else:
        return False


# ============================
# Routes
# ============================


# Homepage
@app.route("/")
def index():
    db = get_db()
    etablissements = db.get_all_etablissements()
    return render_template("index.html", etablissements=etablissements), 200


# Search for violations
@app.route("/search_violations")
def search_violations():
    db = get_db()
    criteria = request.args.get("criteria")
    search_type = request.args.get("search_type")
    results_s = []
    if criteria != "" and search_type in [
        "etablissement",
        "proprietaire",
        "rue",
    ]:
        results_s = db.get_violations_from_search(criteria, search_type)
    else:
        return render_template("index.html"), 200

    return (
        render_template("violations.html", violations_search=results_s),
        200,
    )


# not done
# login
@app.route("/login", methods=["GET", "POST"])
def login():
    db = get_db()
    if request.method == "GET":
        return render_template("login.html"), 200

    login_data = request.form
    username = login_data.get("username")
    password = login_data.get("password")

    if verify_password(username, password):
        session["authenticated"] = True
        return render_template("user_options.html"), 200
        # ICI todo
        # return render_template("user_options.html"), 200
        # return basic_auth.login_required(render_template(
        #     "user_options.html")), 200
    else:
        error = "Nom d'utilisateur ou mot de passe invalide"
        return render_template("login.html", error=error), 400


# Registration
@app.route("/registration")
def registration():
    return render_template("registration.html"), 200


# Inspection request
@app.route("/inspection")
def inspection():
    return render_template("demande_inspection.html"), 200


# ======
# API
# ======


# API documentation
@app.route("/api/doc")
def apidoc():
    return render_template("doc.html")


# ================
# API - Violations
# ================


# Get violations between dates
# (ex: /api/violations?du=2022-01-01&au=2023-01-01)
@app.route("/api/violations", methods=["GET"])
def get_violations_between_dates():
    start_date = request.args.get("du")
    end_date = request.args.get("au")

    if start_date and end_date:
        try:
            datetime.fromisoformat(start_date)
            datetime.fromisoformat(end_date)
        except ValueError:
            return (
                jsonify({"message": get_error_message("invalid_date_format")}),
                400,
            )

        db = get_db()
        formatted_start_date = start_date.replace("-", "")
        formatted_end_date = end_date.replace("-", "")
        violations = db.get_violations_between_dates(
            formatted_start_date, formatted_end_date
        )

        if violations:
            v_list = [violation.asDictionary() for violation in violations]
            return jsonify(v_list), 200
        else:
            return (
                jsonify({"message":
                        get_error_message("no_violations_found_dates")}),
                404,
            )
    else:
        return (
            jsonify({"message": get_error_message("bad_request")}),
            400,
        )


# Delete all violations from buisness_id
@app.route("/api/delete_violations/<buisness_id>", methods=["DELETE"])
@basic_auth.login_required
# @login_required
def delete_all_violations_by_buisness_id(buisness_id):
    db = get_db()
    deleted_violations = db.get_violations_by_buisness_id(buisness_id)
    db.delete_violations_by_buisness_id(buisness_id)
    write_violations_to_csv(deleted_violations,
                            "db/log/deleted_violations.csv")
    return (
        jsonify({"message": get_error_message("violations_delete_success")}),
        200,
    )


# Update all violations (name) from buisness_id
@app.route("/api/update_violations/<buisness_id>", methods=["PUT"])
@basic_auth.login_required
@schema.validate(update_contrevenant_schema)
def modify_all_violations_by_buisness_id(buisness_id):
    try:
        data = request.get_json()
        new_etablissement = data.get("etablissement")
        db = get_db()
        db.update_etablissement_by_buisness_id(buisness_id, new_etablissement)
        updated_violations = db.get_violations_by_buisness_id(buisness_id)
        write_violations_to_csv(updated_violations,
                                "db/log/updated_violations.csv")

        return (
            jsonify({"message":
                    get_error_message("violations_update_success")}),
            200,
        )
    except Exception as e:
        return jsonify({"message": get_error_message("internal_error")}), 500


# Get violations from one etablissement
@app.route("/api/violations/<buisness_id>", methods=["GET"])
def get_all_violations_by_buisness_id(buisness_id):
    db = get_db()
    violations = db.get_violations_by_buisness_id(buisness_id)
    if violations:
        v_list = [violation.asDictionary() for violation in violations]
        return jsonify(v_list), 200
    else:
        return (
            jsonify({"message":
                    get_error_message("no_violations_for_business_id")}),
            404,
        )


# Get violations summary JSON (# of infractions by etablissement)
@app.route("/api/violations/summary.json", methods=["GET"])
def get_violations_summary_json():
    db = get_db()
    violations_summary = db.get_violations_summary()

    if not violations_summary:
        return jsonify({"message": get_error_message("no_violations")}), 404

    summ_list = [summ.asDictionary() for summ in violations_summary]
    return jsonify(summ_list), 200


# Get violations summary XML (# of infractions by etablissement)
@app.route("/api/violations/summary.xml", methods=["GET"])
def get_violations_summary_xml():
    db = get_db()
    violations_summary = db.get_violations_summary()
    if not violations_summary:
        return jsonify({"message": get_error_message("no_violations")}), 404

    summ_list = [summ.asDictionary() for summ in violations_summary]
    xml_data = dict_to_xml(summ_list)
    return xml_data, 200


# Format to xml
def dict_to_xml(dictionary):
    root = Element("all_violations_summary")
    for item in dictionary:
        entry = SubElement(root, "violation_summary")
        for key, value in item.items():
            SubElement(entry, key).text = str(value)
    xml_str = tostring(root, encoding="utf-8",
                       method="xml", xml_declaration=True)
    xml_str = parseString(xml_str).toprettyxml(indent="  ")
    return xml_str


# Get violations summary CSV (# of infractions by etablissement)
@app.route("/api/violations/summary.csv", methods=["GET"])
def get_violations_summary_csv():
    db = get_db()
    violations_summary = db.get_violations_summary()
    if not violations_summary:
        return jsonify({"message": get_error_message("no_violations")}), 404

    summary = [summ.asDictionary() for summ in violations_summary]
    csv_data = dict_to_csv(summary)
    return csv_data, 200


# Format to csv
def dict_to_csv(dictionary):
    try:
        output = StringIO()
        fieldnames = dictionary[0].keys() if dictionary else []
        writer = csv.DictWriter(output, fieldnames=fieldnames)

        writer.writeheader()
        for item in dictionary:
            writer.writerow(item)

        csv_string = output.getvalue()
        output.close()
        return csv_string
    except Exception as e:
        return f"Error converting to CSV string: {e}"


# ==================
# API - Inspections
# ==================


# Post inspection request
@app.route("/api/demande_inspection", methods=["POST"])
@schema.validate(insert_demande_inspection_schema)
def create_demande_inspection():
    db = get_db()
    try:
        data = request.get_json()

        di = DemandeInspection(
            None,
            data["etablissement"],
            data["adresse"],
            data["ville"],
            data["date_demande"],
            data["nom_client"],
            data["description_demande"],
        )

        db.insert_demande_inspection(
            di.etablissement,
            di.adresse,
            di.ville,
            di.date_demande.strftime("%Y-%m-%d"),
            di.nom_client,
            di.description_demande,
        )

        return jsonify(di.as_dict()), 201

    except Exception as e:
        return (
            jsonify({"message": get_error_message("internal_error")}),
            500,
        )


# Delete inspection request
@app.route("/api/demande_inspection/<id_demande>", methods=["DELETE"])
def delete_inspection_request(id_demande):
    db = get_db()
    db.delete_inspection_request(id_demande)
    return (
        jsonify({"message": get_error_message("inspection_delete_success")}),
        200,
    )


# ============
# API - Users
# ============


# Post new user
@app.route("/api/create_user", methods=["POST"])
@schema.validate(insert_user_schema)
def create_new_user():
    db = get_db()
    try:

        data = request.get_json()

        if db.username_exist(data["username"]):
            return (
                jsonify({"message": "Username already exists"}),
                400,
            )

        new_user = User(
            data["nom"],
            data["prenom"],
            data["username"],
            data["email"],
            data["password"],
            data["etablissements"],
        )

        salt = uuid.uuid4().hex
        hashed_pw = hashlib.sha512(
            str(new_user.password + salt).encode("utf-8")
        ).hexdigest()
        etablissements_str = ",".join(data["etablissements"])

        db.insert_user(
            new_user.nom,
            new_user.prenom,
            new_user.username,
            new_user.email,
            salt,
            hashed_pw,
            etablissements_str,
        )

        return jsonify(new_user.as_dict()), 201

    except Exception as e:
        return (
            jsonify({"message": get_error_message("internal_error")}),
            500,
        )


# ===========
# Main
# ===========

if __name__ == "__main__":
    app.run(debug=True)
