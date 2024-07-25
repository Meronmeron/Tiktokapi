from flask import Flask, request, jsonify,send_file
import requests
from flask_cors import CORS
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

import os
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}) 
CORS(app)  # Enable CORS for all routes # Enable CORS for the /api/* endpoints
UPLOAD_FOLDER = 'uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/creator_info', methods=['POST'])
def get_creator_info():
    url = 'https://open.tiktokapis.com/v2/post/publish/creator_info/query/'
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Authorization header is missing"}), 400

    headers = {
        'Authorization': auth_header,
        'Content-Type': 'application/json; charset=UTF-8'
    }
    response = requests.post(url, headers=headers)
    return jsonify(response.json())
@app.route('/api/upload', methods=['POST'])
def upload_files():
    video_file = request.files.get('video')
    creative_file = request.files.get('creative')
    sliderValue = int(request.form.get('position_value'))
    horizontal_value = int(request.form.get('horizontal_value'))
    width_value = int(request.form.get('width_value'))
    height_value = int(request.form.get('height_value'))
    start_time = float(request.form.get('start_time', 0))
    end_time = float(request.form.get('end_time', None))
    video_dimension = request.form.get('video_dimension')
    animation_type = request.form.get('animation_type', 'none')
    animation_duration = float(request.form.get('animation_duration'))
    
    video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
    creative_path = os.path.join(UPLOAD_FOLDER, creative_file.filename)
    video_file.save(video_path)
    creative_file.save(creative_path)
    output_path = os.path.join(UPLOAD_FOLDER, 'output.mp4')
    
    width, height = map(int, video_dimension.split('x'))
    process_video(video_path, creative_path, sliderValue, horizontal_value, width_value, height_value, start_time, end_time, output_path, animation_duration, animation_type, width, height)

    # return jsonify({'output_path': output_path})
    return send_file(output_path, as_attachment=True, download_name='edited_video.mp4')

def process_video(video_path, creative_path, sliderValue, horizontal_value, width_value, height_value, start_time, end_time, output_path, animation_duration, animation_type, width, height):
    video = VideoFileClip(video_path).resize(newsize=(width, height))
    creative = (VideoFileClip(creative_path) if creative_path.lower().endswith(('mp4', 'avi', 'mov'))
                else ImageClip(creative_path).set_duration(video.duration))

    y = sliderValue * int(height - height_value) / 100
    x = horizontal_value * int(width - width_value) / 100
    # let x = parseInt(horizontalValue) * (canvas.width - parseInt(widthValue)) / 100
    # let y = (parseInt(sliderValue) * (canvas.height - parseInt(heightValue))) / 100
    creative = creative.resize(newsize=(width_value, height_value))
    creative = creative.set_start(start_time)
    creative = creative.set_position((x,y))
    if end_time:
        creative = creative.set_end(end_time)
        
    creative_width, creative_height = creative.size 

    if animation_type == 'fadein':
        creative = creative.fadein(animation_duration)
    elif animation_type == 'fadeout':
        creative = creative.fadeout(animation_duration)   
    elif animation_type == 'slide':
        creative = creative.set_position(lambda t: (0 if t < start_time else int((t - start_time) * (width - creative.size[0]) / (end_time - start_time)), y))        
        final = CompositeVideoClip([video, creative])
        final.write_videofile(output_path, codec='libx264')
        return


    final = CompositeVideoClip([video, creative])
    final.write_videofile(output_path, codec='libx264')
    # return jsonify({"output_path": f"/temp/{os.path.basename(output_path)}"}), 200

@app.route('/api/post', methods=['POST'])
def upload_video():
    if 'video_file' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video_file = request.files['video_file']
    output_path = os.path.join('uploads', video_file.filename)  # Adjust path as needed

    video_file.save(output_path)
    access_token = request.headers.get('Authorization')
    if not access_token:
        return jsonify({'error': 'No access token provided'}), 400
    
    upload_init_url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"


    video_size = os.path.getsize(output_path)
    min_chunk_size = 5 * 1024 * 1024  # 5 MB
    chunk_size = min(min_chunk_size, video_size)
    total_chunk_count = (video_size + chunk_size - 1) // chunk_size  # Ceiling division

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; charset=UTF-8'
    }

    data = {
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": video_size,
            "chunk_size": chunk_size,
            "total_chunk_count": total_chunk_count
        }
    }

    response = requests.post(upload_init_url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        upload_url = response_data['data']['upload_url']

        with open(file_path, 'rb') as video_file:
            for chunk_index in range(total_chunk_count):
                start_byte = chunk_index * chunk_size
                end_byte = min(start_byte + chunk_size, video_size) - 1
                video_file.seek(start_byte)
                chunk_data = video_file.read(end_byte - start_byte + 1)

                content_range = f'bytes {start_byte}-{end_byte}/{video_size}'
                headers = {
                    'Content-Range': content_range,
                    'Content-Length': str(end_byte - start_byte + 1),
                    'Content-Type': 'video/mp4'
                }

                res = requests.put(upload_url, headers=headers, data=chunk_data)
                print(res)
                if res.status_code not in [200, 201, 202]:
                    return jsonify({'error': f"Failed to upload chunk {chunk_index + 1}"}), 500

        os.remove(output_path)
        return jsonify({'message': 'Video uploaded successfully'})

    else:
        return jsonify({'error': 'Failed to initialize video upload'}), response.status_code
if __name__ == '__main__':
    app.run(debug=True)
