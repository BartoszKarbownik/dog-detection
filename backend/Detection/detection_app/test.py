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

        # model information
        self.model = YOLO("yolov8n.pt")

        # visual information
        self.annotator = None
        self.start_time = 0
        self.end_time = 0

        # device information
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

    def predict(self, im0):
        """Run prediction using a YOLO model for the input image `im0`."""
        results = self.model(im0)
        return results


    def plot_bboxes(self, results, im0):
        """Plots bounding boxes on an image given detection results; returns annotated image and class IDs."""
        class_ids = []
        self.annotator = Annotator(im0, 3, results[0].names)
        boxes = results[0].boxes.xyxy.cpu()
        clss = results[0].boxes.cls.cpu().tolist()
        names = results[0].names
        for box, cls in zip(boxes, clss):
            class_ids.append(cls)
            self.annotator.box_label(box, label=names[int(cls)], color=colors(int(cls), True))
        return im0, class_ids

    # def plot_boxes(self, results, im0):
    #     boxes = results[0].boxes.xyxy.cpu()
    #     clss = results[0].boxes.cls.cpu().tolist()
    #     names = results[0].names
    #     for box, cls in zip(boxes, clss):
    #         if names[int(cls)] == 'person':
    #             cv2.imwrite('person_detected.jpg', im0)

    def __call__(self):
        """Executes object detection on video frames from a specified camera index, plotting bounding boxes and returning modified frames."""
        cap = cv2.VideoCapture(self.capture_index)
        assert cap.isOpened()
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        frame_count = 0
        while True:
            self.start_time = time()
            ret, im0 = cap.read()
            assert ret
            results = self.predict(im0)
            im0, class_ids = self.plot_bboxes(results, im0)

            cv2.imshow('YOLOv8 Detection', im0)
            frame_count += 1
            if cv2.waitKey(5) & 0xFF == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

detector = ObjectDetection(capture_index=0)
detector()
# import cv2
# from PIL import Image
# import os
# from datetime import datetime
# from ultralytics import YOLO

# # Initialize the YOLO model
# model = YOLO('yolov8n.pt')

# # Define the directory to save screenshots
# save_directory = "C:/Users/Bartek/Desktop/Detection/screenshots"
# if not os.path.exists(save_directory):
#     os.makedirs(save_directory)

# # Start capturing video from the webcam
# cap = cv2.VideoCapture(0)

# try:
#     while True:
#         # Capture frame-by-frame
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Convert the frame from BGR to RGB (required for the model)
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
#         # Perform inference
#         results = model(rgb_frame)

#         # Check for 'dog' in the detected classes
#         dog_detected = any('dog' in model.names[int(result['class'])] for result in results)

#         if dog_detected:
#             # Convert RGB frame back to BGR for saving/displaying
#             bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
#             # Generate a unique filename with a timestamp
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             file_path = os.path.join(save_directory, f'dog_detected_{timestamp}.png')
#             # Save the frame as an image file when a dog is detected
#             img = Image.fromarray(bgr_frame)
#             img.save(file_path)
        
#         # Show the frame
#         cv2.imshow('Webcam Feed', frame)
        
#         # Break the loop with 'q' key
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
# finally:
#     # When everything done, release the capture
#     cap.release()
#     cv2.destroyAllWindows()
