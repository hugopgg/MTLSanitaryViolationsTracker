# ============================================
# Auteur: Hugo Perreault Gravel 
# ============================================

from dateutil import parser

# =========================
# Model for a Violation
# =========================


class Violation:
    def __init__(
        self,
        id_poursuite,
        buisness_id,
        date,
        description,
        adresse,
        date_jugement,
        etablissement,
        montant,
        proprietaire,
        ville,
        statut,
        date_statut,
        categorie,
    ):
        self.id_poursuite = id_poursuite
        self.buisness_id = buisness_id
        self.date = parser.parse(str(date))
        self.description = description
        self.adresse = adresse
        self.date_jugement = parser.parse(str(date_jugement))
        self.etablissement = etablissement
        self.montant = montant
        self.proprietaire = proprietaire
        self.ville = ville
        self.statut = statut
        self.date_statut = parser.parse(str(date_statut))
        self.categorie = categorie

    def asDictionary(self):
        return {
            "id_poursuite": self.id_poursuite,
            "buisness_id": self.buisness_id,
            "date": self.date.strftime("%Y-%m-%d"),
            "description": self.description,
            "adresse": self.adresse,
            "date_jugement": self.date_jugement.strftime("%Y-%m-%d"),
            "etablissement": self.etablissement,
            "montant": self.montant,
            "proprietaire": self.proprietaire,
            "ville": self.ville,
            "statut": self.statut,
            "date_statut": self.date_statut.strftime("%Y-%m-%d"),
            "categorie": self.categorie,
        }
