#!/usr/bin/env python3

# Imports ---------------------------------------------------------------------

from pathlib import Path
import os
import shutil

# Constants -------------------------------------------------------------------

working_path = Path('AmsContainer')

# Functions -------------------------------------------------------------------


# Main ------------------------------------------------------------------------

if __name__ == "__main__":
    
    # Had to to create list here, or paths would not resolve in for loop
    # for some reason or other
    pdf_paths = list(working_path.glob('**/fulltext.pdf'))

    container_0 = working_path.joinpath('AmsContainer_0')
    container_1 = working_path.joinpath('AmsContainer_1')
    container_2 = working_path.joinpath('AmsContainer_2')
    container_3 = working_path.joinpath('AmsContainer_3')
    
    try:
        os.mkdir(container_0)
        os.mkdir(container_1)
        os.mkdir(container_2)
        os.mkdir(container_3)
    except:
        pass # Fail silently

    for i, pdf_path in enumerate(pdf_paths):
        try:
            if i % 4 == 0:
                shutil.move(pdf_path.parent, container_0.joinpath(pdf_path.parent.name))
            elif i % 4 == 1:
                shutil.move(pdf_path.parent, container_1.joinpath(pdf_path.parent.name))
            elif i % 4 == 2:
                shutil.move(pdf_path.parent, container_2.joinpath(pdf_path.parent.name))
            else:
                shutil.move(pdf_path.parent, container_3.joinpath(pdf_path.parent.name))
        except:
            print(f'Could not move PMC: {pdf_path.parent.name}')
