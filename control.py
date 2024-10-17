#!/usr/bin/env python
# -*- coding:utf-8 -*-
#import math
import rospy
from std_msgs.msg import Float32, String
from geometry_msgs.msg import Twist
import numpy as np

class move_control:
    def __init__(self):

        rospy.init_node('control', anonymous=True)

        self.BASE_SPEED = 10
        self.yellow_center_x = 320 ## 수정
        self.center_x = 320
        self.old_x = 0 ##0430 self.old_x -&gt; self.error_x
        self.order_x = 0 ##0430 self.order_x -&gt; self.steer
        self.sonar_L= 0
        self.sonar_R= 0
        self.len_sonar_L = 0 ## self.list_sonar_L 리스트 원소 중 30 이상 원소 개수 변수 추가
        self.len_sonar_R = 0 ## self.list_sonar_R 리스트 원소 중 30 이상 원소 개수 변수 추가
        self.list_sonar_L = [] ## 왼쪽 초음파 센서값 5개씩 저장할 리스트 초기화
        self.list_sonar_R = [] ## 오른쪽 초음파 센서값 5개씩 저장할 리스트 초기화

        #rospy.Subscriber("/lane/center_lane_x", Int32, self.lane_C_cb)
        rospy.Subscriber("/lane/center_lane_x", Float32,self.lane_C_cb)
        rospy.Subscriber("/sonar_L", Float32,self.sonar_L_cb)
        rospy.Subscriber("/sonar_R", Float32,self.sonar_R_cb)
        #self.drive_pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)
        self.drive_pub1 = rospy.Publisher("cmd_vel", Float32, queue_size=1)
        self.drive_pub2 = rospy.Publisher("cmd_steer", Float32, queue_size=1)
        rospy.Timer(rospy.Duration(0.033), self.drive_control)

    def drive_control(self, event):
        ## 장애물 기준 : 30cm 이내
        if self.len_sonar_L &gt; 3 and self.len_sonar_R &gt; 3 : ## 장애물 발견 안된 경우

            self.error_x = self.yellow_center_x-self.center_x ##0430 self.old_x -&gt; self.error_x
            self.steer= self.error_x*0.025 #0넣으면 직진 ##0430 self.order_x -&gt; self.steer, 0.025 너무 작은 듯 함.
            if self.steer &gt;= 0:                   ##0430 추가
	              self.steer= min(self.steer,40)    ##0430 추가
            else:                                 ##0430 추가
                self.steer = max(self.steer,-40)  ##0430 추가

            #self.order_x = 0 ## 직진으로 테스트 (추후 삭제)
            self.drive_pub1.publish(self.BASE_SPEED)
            self.drive_pub2.publish(self.steer)
            print("장애물 없음")

        else: ## 장애물이 발견된 경우

            self.drive_pub1.publish(0) ## 수정
            self.drive_pub2.publish(0) ## 추가
            print("장애물 발견")
                  
    def lane_C_cb(self, data):

        if data.data == 0:
            self.yellow_center_x = 320
        else:
            self.yellow_center_x = data.data

    def sonar_L_cb(self, data):

        self.sonar_L = data.data                    ## 왼쪽 초음파 센서 값 저장

        if len(self.list_sonar_L) == 5:             ## list_sornar_L 리스트 원소 개수가 5개이면 

            self.list_sonar_L.pop(0)                ## 오래된 센서값 제거 
            self.list_sonar_L.append(self.sonar_L)  ## 새로운 센서값 추가
            self.len_sonar_L = len(list(filter(lambda n : n &gt; 30 ,self.list_sonar_L))) ## 5개의 원소 중 30 이상 갯수 검출  

        else:

            self.list_sonar_L.append(self.sonar_L)
        
         
    def sonar_R_cb(self, data):

        self.sonar_R = data.data                    ## 왼쪽 초음파 센서 값 저장

        if len(self.list_sonar_R) == 5:             ## list_sornar_L 리스트 