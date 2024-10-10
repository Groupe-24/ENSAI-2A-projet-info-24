class Utilisateur:
    def __init__(self, id, nom, mail, ddn, mdp=None, administrateur=False, organisateur=False):
        """Constructeur"""
        self.id_utilisateur = id
        self.nom = nom
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
            f"ID: {self.id_utilisateur}, Nom: {self.nom}, "
            f"Mail: {self.mail}, Date de Naissance: {self.date_de_naissance}, "
            f"Rôle: {roles_str}"
        )
