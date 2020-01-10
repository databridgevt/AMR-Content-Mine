#/usr/bin/env python3

from pathlib import Path
from shutil import move

wd = Path('AmsContainer')

for i, child in enumerate(wd.iterdir()):
    if i % 3 == 0:
        move(child.as_posix(), wd.joinpath('AmsContainer_0').as_posix())
    elif i % 3 == 1:
        move(child.as_posix(), wd.joinpath('AmsContainer_1').as_posix())
    else:
        move(child.as_posix(), wd.joinpath('AmsContainer_2').as_posix())