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


    def turn_designate_angular(self,massage):

        _total_angular=abs(massage)/2

        #set velocity param
        _velocity=0
        _vel_f=[]
        _vel_s=[]
        _vel_sum=0
        _sign=1/2
        if massage<=0:
            _sign=-_sign
        
        #first half
        _vel_sum,_vel_f=self.set_velocity(_sign,_velocity,_vel_sum,_total_angular)
        
        _velocity=_vel_f[_total_angular]
        
        #second half
        _vel_sum,_vel_s=self.set_velocity(-_sign,_velocity,_vel_sum,_total_angular)
        
        _vel=_vel_f+_vel_s
        #publish
        for i in _vel:
            angular_vel=Twist()
            angular_vel.linear.x=0.0
            angular_vel.angular.z=i/_vel_sum
            self.pub.publish(angular_vel)
        
    @staticmethod
    def set_velocity(sign,velocity,vel_sum,total_angular):
        vel=[]    
        for i in range(1,total_angular+1):
            __acceleration=sign*math.sin(math.radians(i*4*math.pi/total_angular))+sign
            velocity=velocity+__acceleration*math.radians(1)/velocity
            vel.append(2*total_angular*velocity)
            vel_sum=vel_sum+velocity            
        return vel_sum,vel

    def now_angular(self,massage):		
        self.angular = math.degrees(2*math.asin(massage.pose.pose.orientation.z))


def main():
    rclpy.init()
    node = Rotation()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
