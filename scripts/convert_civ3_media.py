from PIL import Image
from typing import Generator
from pathlib import Path
from os import makedirs
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from functools import partial
from itertools import chain

from civ3_utils import get_civ3_path

# glob_art returns an iterator of all paths under the Art folder matching the
# given relative glob (ie. 'terrain/*.pcx').
def glob_art(glob: str) -> Generator[Path, None, None]:
    art = get_civ3_path().joinpath('Art')
    conquests_art = get_civ3_path().joinpath('Conquests/Art')
    return chain(art.glob(glob), conquests_art.glob(glob))

def is_pixel_magenta(tpl: tuple[int]) -> bool:
    return tpl[0] == 255 and tpl[1] == 0 and tpl[2] == 255

def is_pixel_green(tpl: tuple[int]) -> bool:
    return tpl[0] == 0 and tpl[1] == 255 and tpl[2] == 0

def is_pixel_transparent(tpl: tuple[int]) -> bool:
    return is_pixel_magenta(tpl) or is_pixel_green(tpl)

def make_image_transparent(img: Image.Image) -> Image.Image:
    if img.format != 'RGBA':
        img = img.convert('RGBA')
    copy = [p if not is_pixel_transparent(p) else (0, 0, 0, 0) for p in img.getdata()]
    img.putdata(copy)
    return img

def process_file(path: Path, out_dir: Path):
    name = f'{path.name.removesuffix(path.suffix)}.png'
    out_file = Path(out_dir).joinpath(name)
    img = Image.open(path, 'r', ['pcx'])
    img = make_image_transparent(img)
    img.save(out_file)

def convert_pcx_to_png(glob: str, output: Path):
    makedirs(output, exist_ok=True)
    files = glob_art(glob)
    pool = ThreadPool(cpu_count() - 1)
    pool.map(partial(process_file, out_dir=output), files)
    pool.close()
    pool.join()
