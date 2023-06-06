#!python3

'''
This script will create an appmanifest file in your SteamApps folder in order
to force steam to download civ 3 on mac or linux systems.

- run this script with python3
- restart steam
- civ 3 should be in your downloads.
'''

import sys
from pathlib import Path

from civ3_utils import get_os

def create_manifest_content(id, folder):
    return f'''"AppState"
{{
  "AppID"  "{id}"
  "Universe" "1"
  "installdir" "{folder}"
  "StateFlags" "1026"
}}\n'''

STEAMAPPS_LOCATION = {
    'mac': Path().home().joinpath('Library/Application Support/Steam/steamapps/').absolute(),
    'linux': Path().home().joinpath('.steam/steam/SteamApps/').absolute(),
}

CIV3_FOLDER = 'civ3'
CIV3_STEAM_ID = 3910

if __name__ == '__main__':
    folder = CIV3_FOLDER
    if len(sys.argv) > 1:
        folder = sys.argv[1]

    print('creating appmanifest file')
    path = STEAMAPPS_LOCATION[get_os()]
    if not path.exists():
        print('steam apps folder not found')
        sys.exit(1)

    manifest = path.joinpath(f'appmanifest_{CIV3_STEAM_ID}.acf')
    manifest.touch()
    with manifest.open('w', encoding='utf-8') as f:
        f.write(create_manifest_content(CIV3_STEAM_ID, folder))
    print('created appmanifest file')
    print('restart steam to start download')
