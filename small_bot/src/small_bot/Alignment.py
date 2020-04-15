#!/usr/bin/env python

# Imports
import rospy
import pigpio
from geometry_msgs.msg import Point
from support.Constants import *


class Alignment:
    def __init__(self):
        """
        Initializations
        """

        # Initialization of the node
        rospy.init_node('Alignment')

        # Subscribers
        rospy.Subscriber('near_centroid', Point, self.centroid_callback)

        # Connect to local Pi.
        self.pi = pigpio.pi()

        # Configure the Camera Servo
        self.cam_servo_pin = SERVO_CAM
        self.position = 1000
        self.h = 480
        self.w = 500

        self.threshold = 40
        self.twitch = 70

    def centroid_callback(self, msg):
        """
        Callback for the centroid subscriber
        :param msg: Point
        :return: void
        """

        # Centroid from message
        centroid = (msg.x, msg.y)

        # Math for moving the camera
        video_centroid = (self.w / 2, self.h / 2 - 20)
        if centroid[1] > video_centroid[1] + self.threshold:
            self.position -= self.twitch
        elif centroid[1] < video_centroid[1] - self.threshold:
            self.position += self.twitch

        if 2200.0 > self.position > 500.0:
            self.pi.set_servo_pulsewidth(self.cam_servo_pin, self.position)
            rospy.sleep(0.5)

        self.yaw_alignment(centroid)

    def yaw_alignment(self, centroid):
        """
        Moves the motors until we are inline with the can
        :param centroid: the centroid tuple
        :return: void
        """

        
if __name__ == "__main__":
    align_node = Alignment()
    rospy.spin()
