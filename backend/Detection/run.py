from detection_app import create_app
from ultralytics import YOLO

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
