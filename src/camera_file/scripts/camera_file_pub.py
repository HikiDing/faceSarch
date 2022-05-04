#!/usr/bin/env python3
#coding:utf-8

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

if __name__ == '__main__':
    rospy.init_node('img_puber')
    capture = cv2.VideoCapture("/home/hikiqaq/Gungnir_ws/record_39.avi")
    pub = rospy.Publisher('send_pic', Image, queue_size = 10)
    rate = rospy.Rate(10)
    bridge = CvBridge()
    while not rospy.is_shutdown():
        o,image = capture.read()
        pub.publish(bridge.cv2_to_imgmsg(image,"bgr8"))
        cv2.imshow("pub",image)
        if cv2.waitKey(10) == 27:
            break
        rate.sleep()
