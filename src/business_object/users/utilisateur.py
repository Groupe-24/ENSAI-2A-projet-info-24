class Utilisateur:
    def __init__(self, pseudo, id, mail, ddn, mdp=None, administrateur=False, organisateur=False):
        """Constructeur"""
        self.pseudo = pseudo
        self.id = id
        self.mail = mail
        self.date_de_naissance = ddn
        self.mdp = mdp
        self.administrateur = administrateur
        self.organisateur = organisateur

    def __str__(self):
        """Permet d'afficher les informations de l'utilisateur"""
        role = []
        if self.administrateur:
            role.append("Administrateur")
        if self.organisateur:
            role.append("Organisateur")

        roles_str = ", ".join(role) if role else "Utilisateur"

        return (
            f"ID: {self.pseudo}, "
            f"Mail: {self.mail}, Date de Naissance: {self.date_de_naissance}, "
            f"Rôle: {roles_str}"
        )
