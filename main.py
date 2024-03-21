from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SubmitField, FileField
from flask_bootstrap import Bootstrap5
from wtforms.validators import DataRequired
from PIL import Image
import io
import base64
import os
from app import top_most_colors

app = Flask(__name__)
app.config["SECRET_KEY"] = "blablablaaa"
Bootstrap5(app)


class UploadForm(FlaskForm):
    upload = FileField("Upload Your Photo Here.", validators=[DataRequired(), FileAllowed(['jpg'], 'Only JPEG files allowed!')])
    submit = SubmitField("Upload", validators=[DataRequired()])


@app.route("/", methods=["POST", "GET"])
def home():
    image_data = None
    colors = {}
    c = None
    form = UploadForm()
    if form.validate_on_submit():
        image_file = form.upload.data
        file = Image.open(image_file)
        colors, c = top_most_colors(file)
        image_byte_array = io.BytesIO()
        file.save(image_byte_array, format=file.format)
        image_byte_array = image_byte_array.getvalue()
        base64_img = base64.b64encode(image_byte_array).decode('utf-8')
        image_data = f"data:image/{file.format.lower()};base64,{base64_img}"

    return render_template("index.html", form=form, image=image_data, colors=colors, count=c)


if __name__ == "__main__":
    app.run(debug=True)