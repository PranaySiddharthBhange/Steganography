from flask import Flask,jsonify, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from stegano import lsb
from PIL import Image

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hide', methods=['POST'])
def hide_message():
    try:
        if 'image' not in request.files or 'message' not in request.form:
            return jsonify({'error': 'Image or message not provided'}), 400

        image_file = request.files['image']
        message = request.form['message'].strip()

        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400

        if image_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if not allowed_file(image_file.filename):
            return jsonify({'error': 'Invalid file type. Only PNG and JPEG files are allowed'}), 400

        image = Image.open(image_file)
        secret = lsb.hide(image, message)
        output_path = "static/hidden_image.png"
        secret.save(output_path)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        error_message = "Error occurred: " + str(e)
        return redirect(url_for('index', error=error_message))

@app.route('/decode', methods=['POST'])
def decode_message():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Image not provided'}), 400

        image_file = request.files['image']

        if image_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if not allowed_file(image_file.filename):
            return jsonify({'error': 'Invalid file type. Only PNG and JPEG files are allowed'}), 400

        secret = lsb.reveal(image_file)
        return jsonify({'message': secret})

    except Exception as e:
        error_message = "Error occurred: " + str(e)
        return redirect(url_for('index', error=error_message))

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
