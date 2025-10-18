import cv2
import csv

source = cv2.VideoCapture('pendulo.mp4')
fps = source.get(cv2.CAP_PROP_FPS)
data = open('dados.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(data)

frame = source.read()[1]

# Manually select the object that the tracker will follow
cv2.namedWindow("Tracker", cv2.WINDOW_NORMAL)
bbox = cv2.selectROI("Tracker", frame)
color = (204, 255, 0)

# Creating and adding a tracker object
tracker = cv2.legacy.TrackerCSRT_create()
tracker.init(frame, bbox)

# Reference time set as t = 0 at the beginning of the video recording
t = 0.0

while source.isOpened():
    frame = source.read()[1]
    box = tracker.update(frame)[1]

    x = int(box[0])
    y = int(box[1])
    w = int(box[2])
    h = int(box[3])

    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 1, 1)

    # Xc is the coordinate to the bbox center in the x axis
    t += 1/fps
    writer.writerow([t, -0.0788*((x+w*0.5)-0.5*0.025)/68])

    cv2.namedWindow("Object Tracking", cv2.WINDOW_NORMAL)
    cv2.imshow('Object Tracking', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        data.close()
        break
