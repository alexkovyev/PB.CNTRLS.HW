import cv2

from LitteringDetector import LitteringDetector

detector = LitteringDetector()
cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
# out = cv2.VideoWriter('result_video.avi', cv2.cv.CV_FOURCC('M', 'J', 'P', 'G'), 10, (width, height))

img = None
for i in range(5):
    ret, img = cap.read()

detector.train_background(img)

i = 0
while True:
    ret, img = cap.read()
    if not ret:
        break

    #    i += 1
    #    if i % 10 != 0:
    #        continue

    littered = detector(img)
    detector.draw_boxes(img, detector.boxes)

    cv2.putText(img, "Littered" if littered else "Not littered", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 0, 255) if littered else (0, 255, 0), 2)

    # cv2.imshow("img", img)
    # out.write(img)

    # cv2.waitKey(50)
