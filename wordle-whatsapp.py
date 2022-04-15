'''
Provides a way to parse a WhatsApp Chat backup for data about wordles.
For every message it finds in the chat, it looks for the following pattern:
Wordle [\d]{1-4} {1-6X}/6
(exactly 5 Unicode Squares) {1-6}

It then saves the sender's name, the timestamp, the wordle index and its score.
'''

import argparse
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from typing import List

from inputparser.WhatsAppMessageZipParser import WhatsAppMessageZipParser
from WordleStringParser import parseFromSource
from outputsinks.GraphicalOutputs import AverageScore
from outputsinks.WordleOutputSink import WordleOutput

ZIP_ARGUMENT_NAME: str = 'zipPathInput'


def file_path(filePath: str) -> str:
    if os.path.isfile(filePath):
        return os.path.abspath(filePath)
    else:
        raise FileNotFoundError(filePath)

def get_file_path_from_user() -> str:
    return askopenfilename()

parser = argparse.ArgumentParser(description="This is the Wordle WhatsApp Parser.")
parser.add_argument('--input', dest=ZIP_ARGUMENT_NAME, type=file_path, help='The WhatsApp Chat *.zip file')

outputSinks: List[WordleOutput] = [
    AverageScore()
]

if __name__=='__main__':
    print("This is the Wordle WhatsApp Parser.")
    parsed_args = parser.parse_args()
    
    zipFilePath: str = parsed_args.zipPathInput

    if zipFilePath is None:
        zipFilePath = get_file_path_from_user()

    print(f'Zip File path: {zipFilePath}')

    whatsAppParser = WhatsAppMessageZipParser(zipFilePath)
    
    print("Gathering results... ")
    results = list(parseFromSource(whatsAppParser))
    print(f"Done! Got {len(results)} results.")
    print("Outputting results... ")
    for sink in outputSinks:
        sink.output_results(results)
    print("Done!")
