from flask import Flask, request, jsonify, render_template
import json
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Endpoint for handling login
app.debug = True

# Directory for storing uploaded images
UPLOAD_FOLDER = 'posts'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/registration')
def registration():
    return render_template('registration_page.html')


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Here, you can validate the username and password against your JSON file or any other data source
    # Replace this logic with your own implementation

    # Example validation with a JSON file
    with open('users.json') as file:
        users = json.load(file)
        if username in users and users[username] == password:
            return jsonify({'message': 'Login successful'})

    return jsonify({'message': 'Invalid username or password'})


@app.route('/api/post', methods=['POST'])
def create_post():
    # Get the uploaded file
    file = request.files['file']
    if file:
        # Save the file to the posts folder
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Read the existing post JSON file
        post_file = 'post.json'
        posts = {}
        if os.path.exists(post_file):
            with open(post_file) as f:
                posts = json.load(f)

        # Generate a new post ID
        post_id = len(posts) + 1

        # Add the post ID and file name as key-value pairs
        posts[post_id] = filename

        # Write the updated post JSON file
        with open(post_file, 'w') as f:
            json.dump(posts, f)

        return jsonify({'message': 'Post created successfully', 'post_id': post_id})

    return jsonify({'message': 'No file uploaded or invalid file'})


if __name__ == '__main__':
    app.run()
