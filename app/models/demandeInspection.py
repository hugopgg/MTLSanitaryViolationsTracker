# ============================================
# Auteur: Hugo Perreault Gravel 
# ============================================

from dateutil import parser

# ================================
# Model for Inspection Requests
# ================================


class DemandeInspection:
    def __init__(
        self,
        id_demande,
        etablissement,
        adresse,
        ville,
        date_demande,
        nom_client,
        description_demande,
    ):
        self.id_demande = id_demande
        self.etablissement = etablissement
        self.adresse = adresse
        self.ville = ville
        self.date_demande = parser.parse(str(date_demande))
        self.nom_client = nom_client
        self.description_demande = description_demande

    def as_dict(self):
        return {
            "id_demande": self.id_demande,
            "etablissement": self.etablissement,
            "adresse": self.adresse,
            "ville": self.ville,
            "date_demande": self.date_demande.strftime("%Y-%m-%d"),
            "nom_client": self.nom_client,
            "description_demande": self.description_demande,
        }
