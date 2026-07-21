from settings import *
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def import_image(*path, format='png', alpha=True):
    if not pygame.get_init():
        pygame.init()
    full_path = BASE_DIR.joinpath(*path).with_suffix(f'.{format}').resolve()
    image = pygame.image.load(str(full_path))
    if alpha:
        return image.convert_alpha()
    return image.convert()


def import_folder(*path):
    if not pygame.get_init():
        pygame.init()
    frames = []
    folder_path = BASE_DIR.joinpath(*path).resolve()
    for file_name in sorted(folder_path.iterdir(), key=lambda p: int(p.stem)):
        if file_name.is_file():
            frames.append(pygame.image.load(str(file_name)).convert_alpha())
    return frames

def audio_importer(*path):
    if not pygame.get_init():
        pygame.init()

    audio_dict = {}
    supported_extensions = ('.wav', '.mp3', '.ogg')
    folder_path = BASE_DIR.joinpath(*path).resolve()

    if not folder_path.exists():
        return audio_dict

    for file_path in sorted(folder_path.rglob('*')):
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            audio_key = file_path.stem
            audio_dict[audio_key] = pygame.mixer.Sound(str(file_path))

    return audio_dict