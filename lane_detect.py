#! /usr/bin/env python

import cv2
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import Float32
import rospy
from cv_bridge import CvBridge
import time


class LaneDetection:
    def __init__(self):
        rospy.init_node("lane_detect_node")
        self.cvbridge = CvBridge()
        rospy.Subscriber("/main_camera/image_raw", Image, self.Image_process_callback)
        self.lane_C_pub = rospy.Publisher("/lane/center_lane_x", Float32, queue_size=1)
        self.YELLOW_LANE_HIGH = np.array([32,255,255])
        self.YELLOW_LANE_LOW = np.array([25,25,100])
        #rospy.Timer(rospy.Duration(800), self.Image_process_callback)


    def Image_process_callback(self, img):
        self.frame = self.cvbridge.imgmsg_to_cv2(img, "bgr8")
        self.cropped_image_C = self.image_crop_C(self.frame)
        self.thresholded_image_C = self.color_detect_Y(self.cropped_image_C)
        self.yellow_x = self.calc_lane_distance(self.thresholded_image_C)
        print("yellow_x = {}".format(self.yellow_x))

        self.lane_C_pub.publish(self.yellow_x)
        
        viz = True 
        #visualization
        if viz:
            self.viz_result()
           
            
    def calc_lane_distance(self, b_image):
        try:
            M = cv2.moments(b_image)
            self.x = int(M['m10']/M['m00'])
            self.y = int(M['m01']/M['m00'])
        except:
            self.x = 0 ## 0,0이 중앙값이 맞는지?, 0.0 무슨의미인지?
            self.y = 0
        #print("R_x, y  = {}, {}".format(self.R_x, self.R_y))
        return self.x

    def viz_result(self):
        
        cv2.imshow('original image',self.frame)
        self.mask_C = cv2.circle(self.thresholded_image_C,(self.yellow_x,100),10,(0,0,0),-1)
        #cv2.imshow('cropped image_C',self.cropped_image_C)
        #self.mask = cv2.circle(self.center,(320,30),10,(255,0,0),-1)
        cv2.imshow('color_detect_circle_C',self.mask_C)
        #cv2.imshow('car',self.mask)
        cv2.waitKey(1) ## 무슨 코드지
        time.sleep(0.01) ## 빼도될듯
           
    def image_crop_C(self, input_image):
        return input_image[240:480, 0:640]
        
    # def top_view(self, img):
    #     #source = np.float32([[180, 63], [448 , 63], [610, 350],[5, 350]])
    #     source = np.float32([[175, 120], [445 , 120], [3, 300],[603, 300]])
    #     #destination = np.float32([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]])
    #     destination = np.float32([[70, 0], [600, 0], [65, 400], [580, 430  ]])

    #     transform_matrix = cv2.getPerspectiveTransform(source, destination)
    #     minv = cv2.getPerspectiveTransform(destination, source)
    #     img = cv2.warpPerspective(img, transform_matrix, (640, 480))
    #     return img
  


 
    

    def color_detect_Y(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask_yellow = cv2.inRange(hsv, self.YELLOW_LANE_LOW, self.YELLOW_LANE_HIGH)
        return mask_yellow
        
        
        



if __name__ == '__main__':
    a = LaneDetection()
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("program down")