import urllib.request
from loguru import logger
from pathlib import Path


## Global Constants
DEST_DIR = 'data/'

if not Path(DEST_DIR).exists():
    Path(DEST_DIR).mkdir()

def target_exists(target_path):
    try:
        with open(target_path) as f:
            return True
    except FileNotFoundError:
        return False

def download(url, target_path, force_download=False):
    if target_exists(target_path) and not force_download:
        logger.info(f'{target_path} already exists. Skipping download.')
        return
    urllib.request.urlretrieve(url, target_path)


## The Verdict - Book
THE_VERDICT_URL_BY_BOOK = ("https://raw.githubusercontent.com/rasbt/"
    "LLMs-from-scratch/main/ch02/01_main-chapter-code/"
    "the-verdict.txt")
THE_VERDICT_FILE = DEST_DIR + 'the_verdict.txt'

def download_the_verdict(url=THE_VERDICT_URL_BY_BOOK, force_download=False):
    download(url, THE_VERDICT_FILE, force_download)
