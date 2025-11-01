import cv2

cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Camera not accessible 😢")
else:
    print("Camera found ✅")
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Frame not received")
            break
        cv2.imshow("Camera Test", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cam.release()
cv2.destroyAllWindows()
