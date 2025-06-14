from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64
from pytesseract import pytesseract

pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Optional: Uncomment to apply thresholding
    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return gray

def recognize_text(image):
    return pytesseract.image_to_string(Image.fromarray(image), config='--psm 6').strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture_text', methods=['POST'])
def capture_text():
    if 'image' in request.files:
        file = request.files['image']
        image = Image.open(file.stream)
    else:
        try:
            data = request.get_json()
            base64_image = data['image'].split(',')[1]
            image_data = base64.b64decode(base64_image)
            image = Image.open(BytesIO(image_data))
        except Exception:
            return jsonify({'error': 'Invalid image data'}), 400

    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    processed_image = preprocess_image(image)
    extracted_text = recognize_text(processed_image)

    return jsonify({'text': extracted_text})

if __name__ == '__main__':
    app.run(debug=True)
