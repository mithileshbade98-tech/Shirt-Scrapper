from flask import Flask, request
import os

app = Flask(__name__)

base_path = "/Users/mithileshbade/Desktop/SELF PROJECTS AND COURSES/flaskml"
directory_path = os.path.join(base_path, "some_directory")

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
        filepath = os.path.join(directory_path, file.filename)
        file.save(filepath)
        return 'File uploaded and saved.'

if __name__ == '__main__':
    app.run(debug=True)
