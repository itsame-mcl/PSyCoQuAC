from ViewLayer.CLI.start_view import StartView
import dotenv


if __name__ == '__main__':
    dotenv.load_dotenv(override=True)
    vue_actuelle = StartView()
    while vue_actuelle:
        with open('assets/bordure.txt', 'r') as border:
            print(border.read())
            vue_actuelle.display_info()
            vue_actuelle = vue_actuelle.make_choice()

    with open('assets/terminator.txt', 'r', encoding="utf-8") as arnold:
        print(arnold.read())
