import math
import os

from geometry_msgs.msg import Twist

from modules import calculate_speed

from nav_msgs.msg import Odometry

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String


class Control_System(Node):
    def __init__(self):
        super().__init__('Control_System')
        
        self.angular = 0.0
        self.privious_angular = 0
        self.operator = 0
        self.rotate_flag = True
        self.velocity = 0
        self.velocity_message = Twist()
        
        self.publish_velocity = self.create_publisher(
            Twist,
            'cmd_vel',
            qos_profile_sensor_data
        )

        self.create_subscription(
            String,
            'control_system/command',
            qos_profile_sensor_data,
            self.command_callback
        )
        self.create_subscription(
            Odometry,
            'odom',
            self.now_angular,
            qos_profile=qos_profile_sensor_data
        )
        

    def now_angular(self, message):
        self.angular = math.degrees(2 * math.asin(message.pose.pose.orientation.z))
        print(self.angular)

    def command_callback(self, msg):

        self.command = msg.data
        command = msg.data.split(',')

        if 'rotate' == command[0].replace('Command:', ''):
            self.rotate(float(command[1].replace('Content:', '')))

    def cerebrum_publisher(self, message):
        self.senses_publisher = self.create_publisher(
            String, 'cerebrum/command', qos_profile_sensor_data)

        _trans_message = String()
        _trans_message.data = message

        self.senses_publisher.publish(_trans_message)
        self.destroy_publisher(self.senses_publisher)

    def rotate(self, goal_angular):
        print('rotate')

        self.privious_angular = self.angular

        while self.rotate_flag is True:
            self.operator = calculate_speed.convertor(self.angular, self.privious_angular, self.operator)
            if self.operator == 1:
                self.velocity = calculate_speed.differencer(goal_angular, self.angular+360.0)
            elif self.operator == -1:
                self.velocity = calculate_speed.differencer(goal_angular, self.angular-360.0)
            else:
                self.velocity = calculate_speed.differencer(goal_angular, self.angular)
            print(self.angular)
            if self.velocity == 0:
                print('finish')
                self.rotate_flag = False
                
            self.velocity_message.linear.x = 0.0
            self.velocity_message.angular.z = self.velocity
            self.publish_velocity.publish(self.velocity_message)


def main():
    rclpy.init()
    executor = MultiThreadedExecutor()
    node = Control_System()
    executor.add_node(node)
    rclpy.spin()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
