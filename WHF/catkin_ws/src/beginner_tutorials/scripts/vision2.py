#!/usr/bin/env python

import rospy
import cv2
import numpy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from std_msgs.msg import Float32
from cv_bridge import CvBridge, CvBridgeError


class image_converter:

    def __init__(self):

        cv2.namedWindow("Image window", 1)
        cv2.namedWindow("Image window2", 1)
        cv2.startWindowThread()
        self.bridge = CvBridge()
     
        self.image_sub = rospy.Subscriber("/turtlebot_1/camera/rgb/image_raw",Image, self.callback)
        
        self.pub = rospy.Publisher('/result_topic',String)

        
        
    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            cv_image2 = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError, e:
            print e
            
       # bgr_thresh = cv2.inRange(cv_image,
       #                          numpy.array((200, 230, 230)),
       #                          numpy.array((255, 255, 255)))

        hsv_img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        hsv_thresh = cv2.inRange(hsv_img,
                                 numpy.array((20, 30, 100)),
                                 numpy.array((255, 255, 255)))

  
        
        print numpy.mean(hsv_img[:, :, 0])
        self.pub.publish(str(numpy.mean(hsv_img[:, :, 0])))

        print numpy.mean(hsv_img[:, :, 1])
        self.pub.publish(str(numpy.mean(hsv_img[:, :, 1])))
        
        print numpy.mean(hsv_img[:, :, 2])
        self.pub.publish(str(numpy.mean(hsv_img[:, :, 2])))


       # bgr_contours, hierachy = cv2.findContours(bgr_thresh.copy(),
        #                                          cv2.RETR_TREE,
         #                                         cv2.CHAIN_APPROX_SIMPLE)

        hsv_contours, hierachy = cv2.findContours(hsv_thresh.copy(),
                                                  cv2.RETR_TREE,
                                                  cv2.CHAIN_APPROX_SIMPLE)
        for c in hsv_contours:
            a = cv2.contourArea(c)
            print 'A: ' + str(a)
            if a > 0:
                cv2.drawContours(cv_image, c, -1, (255, 0, 0))
                
        
                
        print '===='
        cv2.imshow("Image window", cv_image)
        cv2.imshow("Image window2",hsv_thresh)

image_converter()
rospy.init_node('image_converter', anonymous=True)
rospy.spin()
cv2.destroyAllWindows()








