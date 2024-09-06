import cv2
import numpy as np
import mediapipe as mp
import pyautogui
from camera_operations import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
isLeft = None
        
#Check whether the hand on screen is left or right
def left_or_right(in_results, in_img):
    if in_results.multi_hand_landmarks:
        for handedness in in_results.multi_handedness:
            if handedness.classification[0].label == "Left":
                isLeft = True
                return isLeft
            else:
                isLeft = False
                return isLeft

#Code for cursor movement
def cursor_movement(cursor_x, cursor_y, index_y, thumb_y):
    if abs(index_y - thumb_y) > 50 and abs(index_y - thumb_y) < 100:
        pyautogui.moveTo(cursor_x, cursor_y)

#Code for left click mouse function
def left_click(index_y, thumb_y):
    if abs(index_y - thumb_y) < 20:
        pyautogui.click()
        pyautogui.sleep(1)
        
#Code for right click mouse function       
def right_click(middle_y, thumb_y):
    if abs(middle_y - thumb_y) < 20:
        pyautogui.rightClick()
        pyautogui.sleep(1)
                        
#Code for scroll function
def scroll(thumb_y, index_y, centerY):
    if index_y - thumb_y <= 20:
        if thumb_y < (centerY - 30) and index_y < (centerY - 30):
            pyautogui.scroll(40)
        elif thumb_y > (centerY + 30) and index_y > (centerY + 30):
            pyautogui.scroll(-40)
    
        
                
    
    