from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    language = SelectField("Language", validators=[DataRequired()])
    word = StringField("Word", validators=[DataRequired()])
    decks = SelectField("Deck", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AnkiForm(FlaskForm):
    image_query = StringField("Image Query")
    notes_front = TextAreaField("Notes Front (side with image)")
    notes_back = TextAreaField("Notes Back (side with word and audio)")
    reverse = BooleanField("Add reverse card (target to original) ?")
    submit = SubmitField("Add to Anki")
