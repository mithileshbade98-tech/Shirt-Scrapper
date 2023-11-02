from flask import Flask, request
from werkzeug.utils import secure_filename
import os
from PIL import Image
import cv2
import numpy as np

app = Flask(__name__)

base_path = "/Users/mithileshbade/Desktop/SELF PROJECTS AND COURSES/flaskml/my_flask_app"
directory_path = os.path.join(base_path, "uploaded_images")

if not os.path.exists(directory_path):
    os.makedirs(directory_path)


@app.route('/', methods=['GET'])
def index():
    return '''
    <!DOCTYPE html>
    <html>
        <title>Image Upload</title>
        <body>
            <h1>Upload an Image</h1>
            <form action="/upload" method="POST" enctype="multipart/form-data">
                <input type="file" name="image">
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    '''


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return 'No file part', 400
    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(directory_path, filename)
        file.save(filepath)

        # Save the extracted shirt image in the my_flask_app directory
        output_path = os.path.join(base_path, "extracted_" + filename)
        extract_shirt_from_image(filepath, output_path)
        return 'File uploaded and processed.'


def extract_shirt_from_image(input_image_path, output_image_path):
    try:
        image = cv2.imread(input_image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            print("No objects detected.")
            return

        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        largest_contour = contours[0]
        mask = np.ones_like(gray) * 255
        cv2.drawContours(mask, [largest_contour], -1, 0, -1)
        shirt_extracted = cv2.bitwise_or(image, image, mask=mask)
        cv2.imwrite(output_image_path, shirt_extracted)
    except Exception as e:
        print("An error occurred:", e)


if __name__ == '__main__':
    app.run(debug=True)
