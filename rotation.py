import os
import math
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from std_msgs.msg import Int8

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class Rotation(Node):
    def __init__(self):
        super(Rotation,self).__init__("Rotation")
        #for getting angular to rotate
        self.create_subscription(Int8,"control_system/rotation",self.turn_designate_angular,qos_profile_sensor_data)

        #for passplanning
        self.pub=self.create_publisher(Twist,"cmd_vel",qos_profile_sensor_data)        
        self.create_subscription(Odometry,"odom",self.now_angular,qos_profile_sensor_data)
        self.angular=None

    def now_angular(self,massage):		
        self.angular = math.degrees(2*math.asin(massage.pose.pose.orientation.z))

    def turn_designate_angular(self,massage):

        #prepare angular in order not to accross 180 line.
        sum=self.angular+massage
        if sum>180:
            sum=sum-360
        if sum<-180:
            sum=sum+360

        total_angular=(sum-self.angular)/2

        #set velocity param
        velocity=0
        vel=[]
        vel_sum=0
        
        #first half
        #acceleration is 1/2sin(4pi/total_angular)+1/2 
        for i in range(1,total_angular+1):
            acceleration=(1/2)*math.sin(math.radians(i*4*math.pi/total_angular))+1/2
            velocity=velocity+acceleration*math.radians(1)/velocity
            vel.append(2*total_angular*velocity)
            vel_sum=vel_sum+velocity
        
        velocity=vel[total_angular]
        
        #second half
        #acceleration is -1/2sin(4pi/total_angular)-1/2
        for i in range(1,total_angular+1):
            acceleration=(-1/2)*math.sin(math.radians(i*4*math.pi/total_angular))-1/2
            velocity=velocity+acceleration*math.radians(1)/velocity
            vel.append(2*total_angular*velocity)
            vel_sum_s=vel_sum_s+velocity

        #publish
        for i in vel:
            angular_vel=Twist()
            angular_vel.linear.x=0.0
            angular_vel.angular.z=vel/vel_sum
            self.pub.publish(angular_vel)

def main():
    rclpy.init()
    node = Rotation()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
