import cv2
import numpy as np
import mediapipe as mp
import pyautogui
from gestures import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

#Draw hand landmarks 
def draw_hands(in_results, in_img):
    if in_results.multi_hand_landmarks:
        for hand_landmarks in in_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
            in_img, 
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
                          
#Main code
def cam_hand_operations():
    cap = cv2.VideoCapture(0)
    handGesture = mp.solutions.hands.Hands()

    
    while cap.isOpened:
        success, image = cap.read()
        if not success:
            print("Empty camera frame")
            continue

        image = cv2.flip(image, 1)
        
        camHeight, camWidth, _ = image.shape
        
        results = handGesture.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        hands = results.multi_hand_landmarks
        
        screenWidth, screenHeight = pyautogui.size()
        
        #Declare the boundaries for mouse movement function within the camera
        roiWidth = 400
        roiHeight = 300
        
        centerY = camHeight / 2

        if hands:
            hand = hands[0]
            
            landmarks = np.array([[lmk.x, lmk.y] for lmk in hand.landmark])
            landmarks[:, 0] *= camWidth
            landmarks[:, 1] *= camHeight

            #Store the position of the used fingers in a variable
            index_pos = landmarks[8]
            thumb_pos = landmarks[4]
            middle_pos = landmarks[12]
            
            #Convert stored position into integer
            index_x, index_y = int(index_pos[0]), int(index_pos[1])
            thumb_x, thumb_y = int(thumb_pos[0]), int(thumb_pos[1])
            middle_x, middle_y = int(middle_pos[0]), int(middle_pos[1])
            
            #Translate the position of the index finger in camera into cursor position on screen
            cursor_x, cursor_y = index_x * (screenWidth / roiWidth), index_y * (screenHeight / roiHeight)

            #Draws circle around index and thumb finger tips
            cv2.circle(img=image, center=(index_x, index_y), radius=10, color=(0, 255, 255))
            cv2.circle(img=image, center=(thumb_x, thumb_y), radius=10, color=(0, 255, 255))
            
            match left_or_right(results, image):
                case True:
                    scroll(thumb_y, index_y, centerY)
                case False:
                    cursor_movement(cursor_x, cursor_y, index_y, thumb_y)
                    left_click(index_y, thumb_y)
                    right_click(middle_y, thumb_y)

        #Call the function to draw hand landmarks
        draw_hands(results, image)
        #Show camera feed
        cv2.imshow('Camera feed', image)
        
        #Press ESC key to exit the program
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
   


