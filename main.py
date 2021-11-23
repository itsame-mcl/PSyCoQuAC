from ViewLayer.CLI.start_view import StartView
from ViewLayer.CLI.setup_view import SetupView
from pathlib import Path
import dotenv


if __name__ == '__main__':
    if Path(".env").is_file():
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file, override=True)
        vue_actuelle = StartView()
    else:
        vue_actuelle = SetupView()
    while vue_actuelle:
        with open('assets/bordure.txt', 'r') as border:
            print(border.read())
            vue_actuelle.display_info()
            vue_actuelle = vue_actuelle.make_choice()

    with open('assets/terminator.txt', 'r', encoding="utf-8") as arnold:
        print(arnold.read())
