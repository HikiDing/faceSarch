#!/usr/bin/env python3
#coding:utf-8

import rospy
import cv2
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image

def callback(data):
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(data,"bgr8")
    cv2.imshow("sub",cv_image)
    cv2.waitKey(10)


if __name__ == '__main__':
    rospy.init_node('img_listener')
    rospy.Subscriber('send_pic', Image, callback)
    rospy.spin()