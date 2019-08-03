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

        finish_flag=False

        while finish_flag==False:
            vel_angular=Twist()
            vel_angular.linear.x=0.0

            total_angular=abs(sum-self.angular)

            if total_angular>10:
                velocity=1
            elif total_angular<=10 and total_angular>3:
                velocity=0.3
            else:
                velocity=0
                finish_flag=True


            if self.angular>sum:
                vel_angular.angular.z=velocity
                self.pub.publish(vel_angular)
            else:
                vel_angular.angular.z=-velocity
                self.pub.publish(vel_angular)

def main():
    rclpy.init()
    node = Rotation()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
