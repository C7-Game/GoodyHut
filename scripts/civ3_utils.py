import sys

from pathlib import Path

def get_os() -> str:
    if sys.platform.startswith('linux'):
        return 'linux'
    elif sys.platform.startswith('darwin'):
        return 'mac'
    raise Exception(f'{sys.platform} is not supported')

def is_folder_civ3(path: Path) -> bool:
    files = path.glob('./civ3id.mb')
    return any(True for _ in files)

def get_civ3_path() -> Path:
    platform = get_os()
    steam_common = 'Library/Application Support/Steam/steamapps/common'
    steam_path = Path.home().joinpath(steam_common)
    if platform in ('linux', 'mac'):
        for folder in steam_path.glob('./*'):
            if is_folder_civ3(folder):
                return folder
    raise Exception(f'could not find civ3 in {steam_path}')
