import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
cap = cv2.VideoCapture(0)

def detect_gesture(hand_landmarks):
    # Store landmark positions
    landmarks = hand_landmarks.landmark

    # Helper: tip IDs for each finger
    tip_ids = [4, 8, 12, 16, 20]

    fingers = []

    # Thumb
    if landmarks[tip_ids[0]].x < landmarks[tip_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other 4 fingers
    for id in range(1, 5):
        if landmarks[tip_ids[id]].y < landmarks[tip_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    total_fingers = fingers.count(1)

    # Gesture rules 👇
    if fingers == [1, 0, 0, 0, 0]:
        return "👍 Thumbs Up"
    elif fingers == [0, 0, 0, 0, 1]:
        return "👎 Thumbs Down"
    elif fingers == [0, 1, 1, 0, 0]:
        return "✌️ Peace"
    elif total_fingers == 5:
        return "🖐️ Open Palm"
    elif total_fingers == 0:
        return "✊ Fist"
    else:
        return None


while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = detect_gesture(hand_landmarks)
            if gesture:
                cv2.putText(frame, gesture, (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                            1.5, (0, 255, 0), 3)

    cv2.imshow("Hand Sign Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
