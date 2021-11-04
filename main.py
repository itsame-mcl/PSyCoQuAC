from ViewLayer.CLI.connexion_view import ConnexionView

if __name__ == '__main__':
    vue_actuelle = ConnexionView()
    while vue_actuelle:
        with open('outils graphiques/bordure.txt', 'r') as border:
            print(border.read())
        vue_actuelle.display_info()
        vue_actuelle = vue_actuelle.make_choice()

    with open('outils graphiques/terminator.txt', 'r', encoding="utf-8") as arnold:
        print(arnold.read())