# ============================================
# Auteur: Hugo Perreault Gravel 
# ============================================

# ===========
# Schemas
# ===========

insert_demande_inspection_schema = {
    "type": "object",
    "required": [
        "etablissement",
        "adresse",
        "ville",
        "date_demande",
        "nom_client",
        "description_demande",
    ],
    "properties": {
        "etablissement": {"type": "string", "maxLength": 100},
        "adresse": {"type": "string", "maxLength": 255},
        "ville": {"type": "string", "maxLength": 50},
        "date_demande": {"type": "string", "format": "date"},
        "nom_client": {"type": "string", "maxLength": 100},
        "description_demande": {"type": "string"},
    },
    "additionalProperties": False,
}


update_contrevenant_schema = {
    "type": "object",
    "required": ["buisness_id", "etablissement"],
    "properties": {
        "buisness_id": {"type": "integer"},
        "etablissement": {"type": "string", "maxLength": 100},
    },
    "additionalProperties": False,
}

insert_user_schema = {
    "type": "object",
    "required": [
        "nom",
        "prenom",
        "username",
        "email",
        "password",
        "etablissements",
    ],
    "properties": {
        "nom": {"type": "string", "maxLength": 50},
        "prenom": {"type": "string", "maxLength": 50},
        "username": {"type": "string", "maxLength": 50},
        "email": {"type": "string", "format": "email", "maxLength": 100},
        "password": {"type": "string", "minLength": 8},
        "etablissements": {
            "type": "array",
            "items": {"type": "string", "maxLength": 100},
        },
    },
    "additionalProperties": False,
}
