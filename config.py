import os


class Config(object):
    SECRET_KEY = "fluent-forever"
    # GOOGLE_IMAGES_LANGUAGE = "French"
    WIKTIONARY_LANGUAGE = "french"
    NUM_GOOGLE_IMAGES = 5
    TEMP_DIR_NAME = "temp"
    TEMP_DIR = os.path.join(os.getcwd(), "app", TEMP_DIR_NAME)
    MAX_IMAGE_SIZE = (400, 400)
    AVAILABLE_LANGUAGES = [
        "Russian",
        "French",
        "English",
        "Spanish",
        "German",
        "Italian",
    ]
    LANGUAGE_CODES = {
        "Russian": "ru",
        "French": "fr",
        "English": "en",
        "Spanish": "es",
        "German": "de",
        "Italian": "it",
    }
