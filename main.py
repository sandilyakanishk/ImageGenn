from flask import Flask, request, render_template, send_file, jsonify
from PIL import Image
from rembg import remove
import io
import openai
from config import key

openai.api_key = key

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/background_remover.html')
def background_remover():
    return render_template('background_remover.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        input_image = Image.open(file.stream)
        output_image = remove_background(input_image)

        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')
    return 'No file uploaded', 400

def remove_background(image):
    # Using rembg library to remove background
    output_image = remove(image)
    return output_image

@app.route('/generateimages/<prompt>')
def generate(prompt):
    print("prompt:", prompt)
    response = openai.Image.create(prompt=prompt, n=5, size="256x256")
    print(response)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
