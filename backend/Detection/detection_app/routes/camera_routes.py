from flask import Response, Blueprint, request, jsonify, current_app, send_file
import cv2
import numpy as np
from sqlalchemy import func
from ultralytics import YOLO
from detection_app.detection import ObjectDetection
from detection_app.models import db, Screenshot
from datetime import datetime, timedelta

camera_blueprint = Blueprint('camera', __name__)

global detection
detection = None

model = YOLO('yolov8n.pt')

@camera_blueprint.route('/start_detection')
def start_detection():
    global detection
    if detection is None:
        detection = ObjectDetection(0, current_app._get_current_object())
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
                ret, buffer = cv2.imencode('.jpg', frame)
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        else:
            blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            ret, buffer = cv2.imencode('.jpg', blank_frame)
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@camera_blueprint.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@camera_blueprint.route('/screenshots', methods=['GET'])
def get_screenshots():
    screenshots = Screenshot.query.order_by(Screenshot.uploaded.desc()).all()
    return jsonify([{
        'id': s.id,
        'filename': s.filename,
        'filepath': s.filepath,
        'expires_at': s.expires_at.isoformat(),
        'uploaded': s.uploaded.isoformat()
    } for s in screenshots])

@camera_blueprint.route('/screenshots/<int:id>', methods=['GET'])
def get_screenshot(id):
    screenshot = Screenshot.query.get_or_404(id)
    return send_file(screenshot.filepath, mimetype='image/jpeg')

def get_status():
    global detection
    if detection is None:
        return {"status": "idle", "error_message": None}
    return detection.get_status()

@camera_blueprint.route('/detection_status')
def detection_status():
    return jsonify(get_status())

@camera_blueprint.route('/stats')
def get_stats():
    total_detections = Screenshot.query.count()
    
    today = datetime.now().date()
    detections_today = Screenshot.query.filter(func.date(Screenshot.uploaded) == today).count()
    
    status = get_status()
    
    return jsonify({
        "total_detections": total_detections,
        "detections_today": detections_today,
        "status": status["status"],
        "error_message": status["error_message"]
    })
    
@camera_blueprint.route('/plain_video_feed')
def plain_video_feed():
    def generate():
        cap = cv2.VideoCapture(0) 
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        cap.release()

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@camera_blueprint.route('/fps')
def get_fps():
    global detection
    if detection and detection.is_running:
        return jsonify({"fps": detection.get_fps()})
    return jsonify({"fps": 0})
