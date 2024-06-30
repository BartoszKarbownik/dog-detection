from flask import Flask, Response
from flask import Blueprint, request, jsonify, current_app
import cv2
from ultralytics import YOLO
from detection_app.detection import ObjectDetection




#app = Flask(__name__) can destroy the app
cap = cv2.VideoCapture(0)  
model = YOLO('yolov8n.pt')
camera_blueprint = Blueprint('camera', __name__)

    
def generate_frames():# legacy
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            results = model(frame, verbose=False)
            frame = results[0]
            # Encode frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Concatenate frame data to make it M-JPEG
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@camera_blueprint.route('/video')
def video():
    detection = ObjectDetection(0)
    
    return Response(detection(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

