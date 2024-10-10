# ============================================
# Auteur: Hugo Perreault Gravel 
# ============================================

# =====================
# Model for Summary
# =====================


class ViolationSummary:
    def __init__(self, etablissement, nombre_infractions):
        self.etablissement = etablissement
        self.nombre_infractions = nombre_infractions

    def asDictionary(self):
        return {
            "etablissement": self.etablissement,
            "nombre_infractions": self.nombre_infractions,
        }
