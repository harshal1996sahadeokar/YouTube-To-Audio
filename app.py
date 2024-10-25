from flask import Flask, request, jsonify, send_file
import os
import yt_dlp
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Ensure a directory exists for saving the audio files
OUTPUT_DIR = 'downloads'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def download_audio(youtube_url: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(OUTPUT_DIR, '%(title)s.%(ext)s')
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        file_name = ydl.prepare_filename(info).replace('.webm', '.mp3')  # For mp3
        return file_name

@app.route('/convert', methods=['POST'])
def convert_video():
    data = request.get_json()
    video_url = data.get('url')

    if not video_url:
        return jsonify({'error': 'No video URL provided!'}), 400

    try:
        audio_file = download_audio(video_url)
        file_name = secure_filename(audio_file)
        return send_file(audio_file, as_attachment=True, download_name=file_name)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
