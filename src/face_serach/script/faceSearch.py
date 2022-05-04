#!/usr/bin/env python3
#!coding=utf-8

from tracemalloc import start
import cv2
from cv2 import circle
import mediapipe as mp
from numpy import imag
import rospy
from sensor_msgs.msg import Image
from uart_process_2.msg import uart_send
import torch
from cv_bridge import CvBridge
from typing import Tuple, Union
import math

_PRESENCE_THRESHOLD = 0.5
_VISIBILITY_THRESHOLD = 0.5


def _normalized_to_pixel_coordinates(
    normalized_x: float, normalized_y: float, image_width: int,
    image_height: int) -> Union[None, Tuple[int, int]]:
  """Converts normalized value pair to pixel coordinates."""

  # Checks if the float value is between 0 and 1.
  def is_valid_normalized_value(value: float) -> bool:
    return (value > 0 or math.isclose(0, value)) and (value < 1 or
                                                      math.isclose(1, value))

  if not (is_valid_normalized_value(normalized_x) and
          is_valid_normalized_value(normalized_y)):
    # TODO: Draw coordinates even if it's outside of the image bounds.
    return None
  x_px = min(math.floor(normalized_x * image_width), image_width - 1)
  y_px = min(math.floor(normalized_y * image_height), image_height - 1)
  return x_px, y_px

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

IMAGE_FILES = []


class SubscribeAndPublish:
    def __init__(self):

        self.__pub_ = rospy.Publisher("uart_send",uart_send,queue_size=10) #发布左上角点和右下角点坐标 (msg.data[0],msg.data[1]),(msg.data[2],msg.data[3])
        self.__sub_ = rospy.Subscriber('send_pic', Image, self.callback)

    def callback(self,data):
        
        global judge_status
        global box_last
        global data_list
        global msg

        cv_img = bridge.imgmsg_to_cv2(data, "bgr8")

        with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:

            image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(image)
    
            # Draw the face mesh annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            idx_to_coordinates = {}
            if results.multi_face_landmarks:       
                for face_landmarks in results.multi_face_landmarks:
                      for idx, landmark in enumerate(face_landmarks.landmark):
                            if ((landmark.HasField('visibility') and
                                landmark.visibility < _VISIBILITY_THRESHOLD) or
                                (landmark.HasField('presence') and
                                    landmark.presence < _PRESENCE_THRESHOLD)):
                                    continue
                            landmark_px = _normalized_to_pixel_coordinates(landmark.x, landmark.y
                                                                            ,640, 480)
                            if(idx == 10):
                                circle(image,landmark_px,10,10)                   
                                msg = uart_send()
                                msg.curYaw =  landmark.x - 0.5
                                msg.curPitch = landmark.y - 0.5
            
            # Flip the image horizontally for a selfie-view display.
            
            self.__pub_.publish(msg)
            cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
            if cv2.waitKey(1) & 0xFF == 27:
                exit(0)

def main():
    rospy.init_node('gungnir', anonymous=True)
    
    global bridge
    global box_last
    global judge_status
    global data_list
    global msg

    box_last = torch.empty(640,480)
    judge_status = 0
    bridge = CvBridge()

    SAP = SubscribeAndPublish()

    rospy.spin()

if __name__ == "__main__":
    main()