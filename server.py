from flask import Flask, render_template
from flask_socketio import SocketIO
from PIL import Image, ImageDraw, ImageFont  
import io
import base64

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')
@socketio.on('connect')  
def handle_connect():  
    print('Client connected')  
    socketio.send('Welcome client!')  
@socketio.on('message')
def handle_message(data):
    header, encoded = data.split(',', 1)
    image_data = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(image_data))
    draw = ImageDraw.Draw(image)  
    text = "Processed Video"  
    font_size = 36  
    font_path = "arial.ttf"
    font_color = (255, 0, 0)  # Red color  
    font = ImageFont.truetype(font_path, font_size) 
    text_position = (10, 10)  # Top-left corner  
    draw.text(text_position, text, fill=font_color, font=font)  
    overlay = Image.new('RGBA', image.size, (255, 0, 0, 128))
    image = Image.alpha_composite(image.convert('RGBA'), overlay)  
    
    
    buffer = io.BytesIO()  
    image.convert('RGB').save(buffer, format="JPEG")  # Convert to 'RGB' to avoid any issues  
    encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')  
    socketio.send(f'data:image/jpeg;base64,{encoded_image}')  

    # Process the image here (e.g., apply filters, detect objects, etc.)
    # processed_image = image  # Modify this line with your processing logic

    # If you want to send the processed image back, encode it again
    # buffer = io.BytesIO()
    # processed_image.save(buffer, format="JPEG")
    # encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    # socketio.send(f'data:image/jpeg;base64,{encoded_image}')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
