import io

import imageio
import numpy as np
from PIL import Image
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


def prepare_image(image, target):
    # if img is not RGB, convert it
    if image.mode != "RGB":
        image = image.convert("RGB")

    image = image.resize(target)
    # image = imagenet_utils.preprocess_input(image)

    return image


@app.route("/load_images", methods=['POST'])
def load_images():
    images = []
    files = request.files.getlist("images[]")
    for file in files:
        image = Image.open(io.BytesIO(file.read()))
        image = prepare_image(image, (299, 299))
        image = np.asarray(image)
        images.append(image)

    imageio.mimsave('static/gif_to_display.gif', images, format='GIF', duration=0.25)

    return render_template('Result.html')


@app.route("/")
def home():
    return render_template('Index.html')


if __name__ == '__main__':
    app.run(port=8086)
