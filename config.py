import os


class Config(object):
    SECRET_KEY = "fluent-forever"
    # GOOGLE_IMAGES_LANGUAGE = "French"
    WIKTIONARY_LANGUAGE = "french"
    NUM_GOOGLE_IMAGES = 5
    TEMP_DIR_NAME = "temp"
    TEMP_DIR = os.path.join(os.getcwd(), "app", TEMP_DIR_NAME)
    MAX_IMAGE_SIZE = (400, 400)
    SIMPLE_WORDS_NOTE_TYPE = "2. Picture Words"
    AVAILABLE_LANGUAGES = ["Russian"]
