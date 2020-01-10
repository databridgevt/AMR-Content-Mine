#!/usr/bin/env python3

import multiprocessing
from pathlib import Path
import subprocess
import sys, os

pdfDirectoryPath = "AmsContainer/"

##########################################
# Data Mining and Collection
##########################################

def process_one(file_path: Path) -> None:
    """ Process PDF at a given Path

    This function take a Path() of a pdf to be parsed. It first calls a subprocess to turn
    the given pdf into a .txt file. This .txt should be stored in the same directory as the
    given pdf. The updateData is called to handel the parsing the .txt file.

    """
    # Get a string name for the file, should be fulltext.pdf
    filename = file_path.name
    # Build a path for the output file
    output_file_path = file_path.parent.joinpath("processed_output.txt")
    # Build the command for processing a pdf. I get string concatenation,
    # But I think .format() is so much nicer when there's multiple arguments

    # Skip if the output file already exists (pdf has already been processed)
    if not output_file_path.exists():
        process_command = "pdf2txt.py -o {to_output} {to_process}".format(
            to_output=output_file_path.as_posix(),
            to_process=file_path.as_posix())

        print('[{}] Processing: {}'.format(os.getpid(), file_path.parent.name))

        subprocess.call(process_command, shell=True)

def process_all() -> None:
    """ Uses Process Pool to Process all PDFs

    This function uses a Process Pool to speed up this script. Essentially,
    This function will create a process for every CPU core available. Then, we pass
    process_one() and a list of all PDFs to the pool.

    """

    # Get a Path Object of the AMS directory
    ams_dir = Path(pdfDirectoryPath)

    # Use pathlib to glob all PDFs from pdfDirectoryPath
    # '**' recursively matches all subdirectories
    pdfs = list(ams_dir.glob('**/fulltext.pdf'))

    print('Found {} PDFs'.format(len(pdfs)))

    # Creating a Process Pool
    pool = multiprocessing.Pool()
    print('Spawned Pool with {} Processes'.format(multiprocessing.cpu_count()))

    # Give Some work to the Pool
    # 30 is called a "chunksize." I think the processes will take pdfs
    # in groups of 30 to process.
    print('Beginning To Convert PDFs to plain text ...')
    
    pool.map(process_one, pdfs, 4)

    print('Finished Converting PDF to plain text...')

    # Politely clean up the Process Pool
    pool.close()
    pool.join()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        pdfDirectoryPath = sys.argv[1]

    process_all()
