import cv2
import mediapipe as mp
import pyautogui
import time
import math
import os
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage

pyautogui.FAILSAFE = False

class GestureController(QThread):
    frame_signal = pyqtSignal(QImage, str, tuple)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        try:
            if getattr(sys, 'frozen', False):
                application_path = os.path.dirname(sys.executable)
            else:
                application_path = os.path.dirname(__file__)

            model_path = os.path.join(application_path, 'gesture_recognizer.task')

            if not os.path.exists(model_path):
                print(f"ERROR: Model file not found at {model_path}")
                return

            BaseOptions = mp.tasks.BaseOptions
            GestureRecognizer = mp.tasks.vision.GestureRecognizer
            GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
            VisionRunningMode = mp.tasks.vision.RunningMode

            options = GestureRecognizerOptions(
                base_options=BaseOptions(model_asset_path=model_path),
                running_mode=VisionRunningMode.VIDEO,
                num_hands=1
            )

            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            cap.set(3, 640)
            cap.set(4, 480)

            last_action_time = 0
            cooldown = 0.6  

            with GestureRecognizer.create_from_options(options) as recognizer:
                while self.running and cap.isOpened():
                    success, frame = cap.read()
                    if not success:
                        break

                    frame = cv2.flip(frame, 1)
                    h, w, _ = frame.shape
                    
                    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    timestamp_ms = int(time.time() * 1000)
                    
                    result = recognizer.recognize_for_video(mp_image, timestamp_ms)

                    action_text = "READY"
                    action_color = (255, 255, 255)
                    is_ok_gesture = False
                    detected_gesture_name = None
                    gesture_score = 0.0

                    if result.hand_landmarks:
                        for hand_landmarks in result.hand_landmarks:
                            points = []
                            for lm in hand_landmarks:
                                cx, cy = int(lm.x * w), int(lm.y * h)
                                points.append((cx, cy))
                                cv2.circle(frame, (cx, cy), 5, (0, 255, 128), cv2.FILLED)
                                cv2.circle(frame, (cx, cy), 2, (255, 255, 255), cv2.FILLED)

                            connections = [
                                (0,1),(1,2),(2,3),(3,4),
                                (0,5),(5,6),(6,7),(7,8),
                                (5,9),(9,10),(10,11),(11,12),
                                (9,13),(13,14),(14,15),(15,16),
                                (13,17),(17,18),(18,19),(19,20),(0,17)
                            ]
                            for p1, p2 in connections:
                                cv2.line(frame, points[p1], points[p2], (255, 128, 0), 2)

                            thumb_tip = hand_landmarks[4]
                            index_tip = hand_landmarks[8]
                            middle_tip = hand_landmarks[12]
                            middle_mcp = hand_landmarks[9]
                            ring_tip = hand_landmarks[16]
                            ring_mcp = hand_landmarks[13]
                            pinky_tip = hand_landmarks[20]
                            pinky_mcp = hand_landmarks[17]

                            dist_thumb_index = math.hypot((thumb_tip.x - index_tip.x)*w, (thumb_tip.y - index_tip.y)*h)
                            
                            middle_up = middle_tip.y < middle_mcp.y
                            ring_up = ring_tip.y < ring_mcp.y
                            pinky_up = pinky_tip.y < pinky_mcp.y

                            if dist_thumb_index < 35 and middle_up and ring_up and pinky_up:
                                is_ok_gesture = True

                    if result.gestures and len(result.gestures) > 0:
                        top_gesture = result.gestures[0][0]
                        detected_gesture_name = top_gesture.category_name
                        gesture_score = top_gesture.score

                    current_time = time.time()
                    if current_time - last_action_time > cooldown:
                        if is_ok_gesture:
                            pyautogui.press('left')
                            action_text = "REWIND 10s (OK Gesture)"
                            action_color = (0, 255, 255)
                            last_action_time = current_time

                        elif detected_gesture_name == "Victory" and gesture_score > 0.4:
                            pyautogui.press('right')
                            action_text = f"FORWARD 10s (Victory) ({gesture_score:.2f})"
                            action_color = (255, 0, 255)
                            last_action_time = current_time

                        elif detected_gesture_name == "Thumb_Up" and gesture_score > 0.45:
                            pyautogui.press('volumeup')
                            action_text = f"VOLUME UP ({gesture_score:.2f})"
                            action_color = (0, 255, 0)
                            last_action_time = current_time

                        elif detected_gesture_name == "Thumb_Down" and gesture_score > 0.45:
                            pyautogui.press('volumedown')
                            action_text = f"VOLUME DOWN ({gesture_score:.2f})"
                            action_color = (0, 165, 255)
                            last_action_time = current_time

                        elif detected_gesture_name == "Closed_Fist" and gesture_score > 0.45:
                            pyautogui.press('space')
                            action_text = f"PLAY / PAUSE ({gesture_score:.2f})"
                            action_color = (0, 0, 255)
                            last_action_time = current_time

                    cv2.rectangle(frame, (10, 10), (450, 60), (30, 30, 30), -1)
                    cv2.rectangle(frame, (10, 10), (450, 60), (100, 100, 100), 1)
                    cv2.putText(frame, f"Action: {action_text}", (20, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.65, action_color, 2)

                    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h_img, w_img, ch = rgb_image.shape
                    qt_image = QImage(rgb_image.data, w_img, h_img, ch * w_img, QImage.Format_RGB888)
                    
                    self.frame_signal.emit(qt_image, action_text, action_color)

            cap.release()
        except Exception as e:
            import traceback
            with open("controller_error.log", "w", encoding="utf-8") as f:
                traceback.print_exc(file=f)

    def stop(self):
        self.running = False
        self.wait()