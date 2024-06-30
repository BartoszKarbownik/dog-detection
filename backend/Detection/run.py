from detection_app import create_app
from ultralytics import YOLO

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, threaded=True)



#checks()
# Load YOLOv9 model
#model = YOLO('yolov8n.pt')

# Predict with the model
#results = model.predict(r'C:\Users\Bartek\Desktop\Detection\dogi.jpg')

#results = model.train(data='data.yaml', epochs=3)

# Enjoy the results!
#results.show()


#print(torch.__version__)