from datetime import datetime
import torch
import numpy as np
import cv2
from time import time
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class ObjectDetection:
    def __init__(self, capture_index):
        """Initializes an ObjectDetection instance with a given camera index."""
        self.capture_index = capture_index
        self.email_sent = False

        self.model = YOLO("yolov8n.pt")

        self.annotator = None
        self.start_time = 0
        self.end_time = 0
        
        self.last_saved_time = datetime.now().timestamp()
        self.save_interval = 3 

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

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

    def __call__(self):
        """Executes object detection on video frames from a specified camera index, plotting bounding boxes and returning modified frames."""
        cap = cv2.VideoCapture(self.capture_index)
        assert cap.isOpened()
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        while True:
            self.start_time = time()
            ret, im0 = cap.read()
            assert ret
            results = self.predict(im0)
            im0, class_ids = self.plot_bboxes(results, im0)
            
            _, buffer = cv2.imencode('.jpg', im0)
            frame = buffer.tobytes()
            #cv2.imshow('YOLOv8 Detection', im0)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')