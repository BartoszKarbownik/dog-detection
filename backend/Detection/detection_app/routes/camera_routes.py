from flask import Flask, Response
from flask import Blueprint, request, jsonify, current_app
import cv2
from ultralytics import YOLO
from detection_app.detection import ObjectDetection
from time import time

global detection
detection = None

#app = Flask(__name__) can destroy the app
cap = cv2.VideoCapture(0)  
model = YOLO('yolov8n.pt')
camera_blueprint = Blueprint('camera', __name__)




@camera_blueprint.route('/start_detection')
def start_detection():
    global detection
    if detection is None:
        detection = ObjectDetection(0)
    detection.start_detection()
    return jsonify({"status": "Detection started"})

@camera_blueprint.route('/stop_detection')
def stop_detection():
    global detection
    if detection:
        detection.stop_detection()
        detection = None
    return jsonify({"status": "Detection stopped"})

def generate_frames():
    global detection
    while True:
        if detection and detection.is_running:
            frame = detection.get_frame()
            if frame is not None:
                # Encode the frame as JPEG
                ret, jpeg = cv2.imencode('.jpg', frame)
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        else:
            # If detection is not running, yield a placeholder or empty frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + b'' + b'\r\n')

@camera_blueprint.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

