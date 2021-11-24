from ViewLayer.CLI.start_view import StartView
from ViewLayer.CLI.setup_view import SetupView
from pathlib import Path
import dotenv


if __name__ == '__main__':
    base_path = Path(__file__).parent
    if Path(base_path / "./.env").is_file():
        dotenv_file = (base_path / "./.env").resolve()
        dotenv.load_dotenv(dotenv_file, override=True)
        vue_actuelle = StartView()
    else:
        vue_actuelle = SetupView(base_path)
    banniere_path = (base_path / "./assets/banniere.txt").resolve()
    with open(banniere_path, 'r', encoding="utf-8") as asset:
        print(asset.read())
    bordure_path = (base_path / "./assets/bordure.txt").resolve()
    while vue_actuelle:
        with open(bordure_path, 'r') as border:
            print(border.read())
            vue_actuelle.display_info()
            vue_actuelle = vue_actuelle.make_choice()

    terminator_path = (base_path / "./assets/terminator.txt").resolve()
    with open(terminator_path, 'r', encoding="utf-8") as arnold:
        print(arnold.read())
