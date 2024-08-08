from datetime import datetime
import torch
import numpy as np
import cv2
from time import time
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
import smtplib
import threading
from queue import Queue

class ObjectDetection:
    def __init__(self, capture_index):
        self.capture_index = capture_index

        self.model = YOLO("yolov8n.pt")

        self.annotator = None
        self.start_time = 0
        self.end_time = 0
        
        self.last_saved_time = datetime.now().timestamp()
        self.save_interval = 3 

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        self.frame_queue = Queue(maxsize=1)
        self.detection_thread = None
        self.is_running = False
        self.latest_frame = None
        self.lock = threading.Lock()

    def predict(self, im0):
        """Run prediction using a YOLO model for the input image `im0`."""
        results = self.model(im0, verbose=False, conf = 0.4)
        return results


    def plot_bboxes(self, results, im0):
        """Plots bounding boxes on an image given detection results; returns annotated image and class IDs."""
        class_ids = []
        current_time = datetime.now().timestamp()
        self.annotator = Annotator(im0, 3, results[0].names)
        boxes = results[0].boxes.xyxy.cpu()
        clss = results[0].boxes.cls.cpu().tolist()
        names = results[0].names
        path = 'C:/Users/Bartek/Desktop/Detection/screenshots'
        
        for box, cls in zip(boxes, clss):
            class_ids.append(cls)
            self.annotator.box_label(box, label=names[int(cls)], color=colors(int(cls), True))
            if names[int(cls)] == 'dog'and (current_time - self.last_saved_time > self.save_interval):
                timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
                filename = f"{path}/dog_detected_{timestamp}.jpg"
                cv2.imwrite(filename, im0)
                self.last_saved_time = current_time  
        return im0, class_ids

    def detection_loop(self):
        cap = cv2.VideoCapture(self.capture_index)
        assert cap.isOpened()
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while self.is_running:
            ret, frame = cap.read()
            if not ret:
                break

            results = self.predict(frame)
            annotated_frame, _ = self.plot_bboxes(results, frame)

            # Make a copy of the annotated frame to avoid shared references
            with self.lock:
                self.latest_frame = annotated_frame.copy()

            if self.frame_queue.full():
                self.frame_queue.get()  # Remove old frame
            self.frame_queue.put(self.latest_frame)

        cap.release()

    def start_detection(self):
        if not self.is_running:
            self.is_running = True
            self.detection_thread = threading.Thread(target=self.detection_loop)
            self.detection_thread.start()

    def stop_detection(self):
        self.is_running = False
        if self.detection_thread:
            self.detection_thread.join()

    def get_frame(self):
        with self.lock:
            if self.latest_frame is not None:
                return self.latest_frame.copy()
            else:
                return None