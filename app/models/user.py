# ============================================
# Auteur: Hugo Perreault Gravel 
# ============================================

# ================================
# Model for User
# ================================


class User:
    def __init__(self, nom, prenom, username, email, password, etablissements):
        self.nom = nom
        self.prenom = prenom
        self.username = username
        self.email = email
        self.password = password
        self.etablissements = etablissements

    def as_dict(self):
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "username": self.username,
            "email": self.email,
            "password": self.password,  # salt + hash?
            "etablissements": self.etablissements,
        }
