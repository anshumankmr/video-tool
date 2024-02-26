from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route('/', methods=['POST'])
def process_video():
    """
    Processes a Video
    """
    try:
        # Get the name from the request data
        video_link = request.json['video_link']
        # Return the greeting with the name
        return f'Hello, {video_link}!'
    except Exception as e:
        return jsonify({'error': str(e)})
    