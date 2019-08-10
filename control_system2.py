import math
import os

from geometry_msgs.msg import Twist

from modules import calculate_speed

from nav_msgs.msg import Odometry

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from std_msgs.msg import String


class Control_System(Node):
    def __init__(self):
        super().__init__('Control_System')

        self.create_subscription(
            String,
            'control_system/command',
            self.command_callback,
            qos_profile_sensor_data
        )

        self.create_subscription(
            Odometry,
            'odom',
            self.odom_crusher,
            qos_profile=qos_profile_sensor_data
        )

        self.pub_vel = self.create_publisher(
            Twist,
            'cmd_vel',
            qos_profile_sensor_data
        )

        self.angular = 0.0
        self.privious_angular = 0
        self.goal_angular = 0

        self.rotate_flag = False

        self.operator = 0
        self.velocity = 0

        self.velocity_message = Twist()

    def command_callback(self, msg):
        print('callback')
        self.command = msg.data
        command = msg.data.split(',')
        if 'rotate' == command[0].replace('Command:', ''):
            self.goal_angular = float(command[1].replace('Content:',''))
            self.rotate_flag = True
        return

    def odom_crusher(self, message):
        prinentation_z = message.pose.pose.orientation.z
        self.angular = math.degrees(2 * math.asin(prinentation_z))
        if self.rotate_flag is True:
            self.operator = calculate_speed.convertor(self.angular,
                                                      self.privious_angular, 
                                                      self.operator)

            if self.operator == 1:
                self.velocity, self.rotate_flag = calculate_speed.differencer(
                                                    self.goal_angular,
                                                    self.angular+360.0,
                                                    self.rotate_flag)
            elif self.operator == -1:
                self.velocity, self.rotate_flag = calculate_speed.differencer(
                                                    self.goal_angular,
                                                    self.angular-360.0,
                                                    self.rotate_flag)
            else:
                self.velocity, self.rotate_flag = calculate_speed.differencer(
                                                    self.goal_angular,
                                                    self.angular,
                                                    self.rotate_flag)
            self.privious_angular = self.angular
            self.velocity_message.angular.z = self.velocity
            self.velocity_message.linear.x = 0.0
            self.pub_vel.publish(self.velocity_message)


def main():
    rclpy.init()
    node = Control_System()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
