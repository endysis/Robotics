#!/usr/bin/env python



"""
Created on Thu Feb 16 11:58:20 2017

@author: computing
"""

import rospy
import cv2
import numpy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from std_msgs.msg import Float32
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist

class Kinematics:
    
    def __init__(self):      
        self.wheel_vel = rospy.Subscriber('/wheel_vel_left',Float32, self.callback)
        self.cmd_vel = rospy.Publisher('/turtlebot_1/cmd_vel', Twist, queue_size = 10)
        
    
    
    def callback(self, data):
        twistMsg = Twist()
        
        left_vel = data.data
        right_vel = 0.0
        
        (v,a) = forward_kinematics(left_vel, right_vel)
        twistMsg.linear.x = v
        twistMsg.angular.z = a
        
        print("\n--- Twist Message ---")        
        print(twistMsg)
        
        self.cmd_vel.publish(twistMsg)
    
            
def forward_kinematics(w_l, w_r):
        wheel_radius = 5
        robot_radius = 0.1
        c_l = wheel_radius * w_l
        c_r = wheel_radius * w_r
        v = (c_l + c_r) / 2
        a = (c_l - c_r) / robot_radius
        return (v, a)
        
    
Kinematics()
rospy.spin()
