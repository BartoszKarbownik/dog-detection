from datetime import datetime
import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
import threading
from queue import Queue
from flask import current_app
import torch
import logging

class ObjectDetection:
    def __init__(self, capture_index, app):
        self.capture_index = capture_index
        self.app = app  
        self.model = YOLO("yolov8n.pt")
        self.annotator = None
        self.last_saved_time = datetime.now().timestamp()
        self.save_interval = 3 
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.frame_queue = Queue(maxsize=1)
        self.detection_thread = None
        self.is_running = False
        self.latest_frame = None
        self.lock = threading.Lock()
        self.screenshot_path = 'C:/Users/Bartek/Desktop/Detection/screenshots'
        self.error_message = None
        self.fps = 0
        self.frame_count = 0
        self.fps_start_time = None


    def save_screenshot(self, filename, filepath):
        with self.app.app_context():
            from detection_app.models import db, Screenshot
            screenshot = Screenshot(filename=filename, filepath=filepath)
            db.session.add(screenshot)
            db.session.commit()

    def plot_bboxes(self, results, im0):
        class_ids = []
        current_time = datetime.now().timestamp()
        self.annotator = Annotator(im0, 3, results[0].names)
        boxes = results[0].boxes.xyxy.cpu()
        clss = results[0].boxes.cls.cpu().tolist()
        names = results[0].names
        
        for box, cls in zip(boxes, clss):
            class_ids.append(cls)
            self.annotator.box_label(box, label=names[int(cls)], color=colors(int(cls), True))
            if names[int(cls)] == 'dog' and (current_time - self.last_saved_time > self.save_interval):
                timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
                filename = f"dog_detected_{timestamp}.jpg"
                file_path = f"{self.screenshot_path}/{filename}"
                cv2.imwrite(file_path, im0)
                self.last_saved_time = current_time
                self.save_screenshot(filename, file_path)

        return im0, class_ids

    def detection_loop(self):
        try:
            cap = cv2.VideoCapture(self.capture_index)
            if not cap.isOpened():
                raise IOError(f"Unable to open video capture with index {self.capture_index}")

            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            self.fps_start_time = datetime.now()

            while self.is_running:
                ret, frame = cap.read()
                if not ret:
                    raise IOError("Failed to grab frame")

                results = self.model(frame, verbose=False)
                annotated_frame, _ = self.plot_bboxes(results, frame)

                with self.lock:
                    self.latest_frame = annotated_frame.copy()

                if self.frame_queue.full():
                    self.frame_queue.get()
                self.frame_queue.put(self.latest_frame)

                self.frame_count += 1
                elapsed_time = (datetime.now() - self.fps_start_time).total_seconds()
                if elapsed_time > 1:
                    self.fps = self.frame_count / elapsed_time
                    self.frame_count = 0
                    self.fps_start_time = datetime.now()

                self.status = 'running'

        except IOError as e:
            self.error_message = str(e)
            self.status = 'error'
            logging.error(f"Camera error: {self.error_message}")
        finally:
            if cap is not None:
                cap.release()
            self.status = 'idle'
            
    def get_fps(self):
        return round(self.fps, 2)

    def start_detection(self):
        if not self.is_running:
            self.is_running = True
            self.error_message = None
            self.status = 'starting'
            self.detection_thread = threading.Thread(target=self.detection_loop)
            self.detection_thread.start()

    def stop_detection(self):
        self.is_running = False
        if self.detection_thread:
            self.detection_thread.join()
        self.status = 'idle'

    def get_frame(self):
        with self.lock:
            if self.latest_frame is not None:
                return self.latest_frame.copy()
            else:
                return None, "No frame available"
            
    def get_status(self):
        return {
            "status": self.status,
            "error_message": self.error_message
        }