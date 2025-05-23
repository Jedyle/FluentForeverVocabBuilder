import os
import re
import json

from flask import render_template, request, jsonify, send_from_directory

from app import app, forms
from app.service import wiktionary, images, anki_connect

ac = anki_connect.AnkiConnect()
save_path_pat = r".*(temp.*)"


@app.route("/")
def index():
    decks = ac.get_deck_names()
    form = forms.SearchForm()
    form.decks.choices = [(i, i) for i in decks]
    form.language.choices = [(l, l) for l in app.config["AVAILABLE_LANGUAGES"]]
    return render_template("index.html", decks=decks, form=form)


@app.route("/search")
def search():
    req = request.args
    word = req.get("word_query")
    deck_name = req.get("deck_name")
    language = req.get("language")
    search_result = wiktionary.search(word, language)
    print("search_result", search_result)
    form = forms.AnkiForm()
    # form.ipa.data = search_result.get("ipa") or ""
    # combo_choices = [
    #     "{}: {}".format(c[0], c[1]) for c in search_result.get("definitions")
    # ]
    # form.word_usage.choices = [(i, i) for i in combo_choices]
    audio_filename = search_result.get("audio_filename")
    if audio_filename:
        audio_relative_filename = re.findall(save_path_pat, audio_filename)[0].replace(
            os.sep, "/"
        )
    else:
        audio_relative_filename = ""
    form.image_query.data = word

    return render_template(
        "search-results.html",
        word=word,
        deck=deck_name,
        form=form,
        audio_filename=audio_relative_filename,
    )


@app.route("/search-images")
def search_images():
    req = request.args
    word = req.get("word_query")
    language = req.get("language")
    page = int(req.get("page", 0))
    image_paths = images.download_images(word, page, language)
    return jsonify(image_paths)


@app.route("/add", methods=["POST"])
def add():
    args = request.values
    word = args.get("word")
    deck = args.get("decks")
    # ipa = args.get("ipa")
    # word_usage = args.get("word_usage")
    audio_arg = args.get("audio_filename")
    if audio_arg:
        audio_filename = os.path.join(app.root_path, audio_arg)
    else:
        audio_filename = None
    json_image_paths = args.get("image_paths")
    parsed_json_image_paths = json.loads(json_image_paths)
    image_paths = list(map(images.format_json_image_path, parsed_json_image_paths))
    thumbnail_image_paths = list(map(images.generate_thumbnail, image_paths))
    notes_front = args.get("notes_front")
    notes_back = args.get("notes_back")
    ac.add_note(
        deck_name=deck,
        word=word,
        image_paths=thumbnail_image_paths,
        notes_front=notes_front,
        notes_back=notes_back,
        recording_file_path=audio_filename,
        reverse=args.get("reverse") or False,
    )
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@app.route("/temp/<path:path>")
def get_temp_file(path):
    return send_from_directory("temp", path)
