import tempfile
import requests
from urllib.request import urlopen
import os
from bs4 import BeautifulSoup

from app import app

cfg = app.config


def get_audio_file_from_html(html):
    soup = BeautifulSoup(html, features="html.parser")
    audiofile = soup.find(class_="audiofile")
    if audiofile is None:
        return None
    if audiofile.find("source") is None:
        return None
    audio_file = soup.find(class_="audiofile").find("source").attrs["src"]
    return "https://" + audio_file.strip("/")  # sometimes the src can start with /


def get_data_from_wiktionary(query, language):
    language_code = "ru"  # hardcoded, TODO CHANGE
    url = f"https://{language_code}.wiktionary.org/wiki"
    response = requests.get(f"{url}/{query}")
    return {"audio": get_audio_file_from_html(response.text)}


def download_audio(url):
    temp_dir = os.path.join(os.getcwd(), cfg["TEMP_DIR"])
    print("url", url)
    data = urlopen(url).read()
    with tempfile.NamedTemporaryFile(
        mode="wb", delete=False, suffix=".ogg", dir=temp_dir
    ) as f:
        f.write(data)
        return f


def search(query, language):
    res = get_data_from_wiktionary(query, language)
    audio_url = res["audio"]
    audio_filename = None
    if audio_url:
        audio_filename = download_audio(audio_url).name
    return {"audio_filename": audio_filename}
