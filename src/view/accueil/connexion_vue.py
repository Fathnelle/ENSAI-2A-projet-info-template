from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from view.menu_administrateur_vue import MenuAdministrateurVue
from view.menu_utilisateur_vue import MenuUtilisateurVue
from view.accueil.accueil_vue import AccueilVue

from service.utilisateur_service import UtilisateurService


class ConnexionVue(VueAbstraite):
    """Vue de Connexion (saisie de pseudo et mdp)"""

    def __init__(self, message=""):
        self.message = message
        self.tentatives_restantes = 3

    def choisir_menu(self):
        while self.tentatives_restantes > 0:
            # Demande à l'utilisateur de saisir pseudo et mot de passe
            pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()
            mdp = inquirer.secret(message="Entrez votre mot de passe :").execute()

            # Appel du service pour trouver l'utilisateur
            user = UtilisateurService().seConnecter(pseudo, mdp)

            # Si l'utilisateur a été trouvé à partir de ses identifiants de connexion
            if user:
                if user.role == "Utilisateur":
                    print(f"\nVous êtes connecté sous le pseudo {user.pseudo}\n")
                    Session().connexion(user)
                    return MenuUtilisateurVue()
                else:
                    print("\nVous êtes connecté en tant qu'administrateur\n")
                    Session().connexion(user)
                    return MenuAdministrateurVue()

            self.tentatives_restantes -= 1
            print(
                f"\nErreur de connexion (pseudo ou mot de passe invalide). "
                f"Tentatives restantes : {self.tentatives_restantes}\n"
            )

        print("Vous avez dépassé le nombre maximum de tentatives.\n")
        return AccueilVue().choisir_menu()
