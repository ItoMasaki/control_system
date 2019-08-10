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
        self.pub_vel = self.create_publisher(
            Twist,
            'cmd_vel',
            qos_profile_sensor_data
        )
        self.angular = 0.0

    def now_angular(self, message):
        prinentation_z = message.pose.pose.orientation.z
        self.angular = math.degrees(2 * math.asin(prinentation_z))
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

        privious_angular = self.angular

        operator = 0
        flag = True

        
        while flag is True:
            operator = calculate_speed.convertor(self.angular, privious_angular, operator)
            if operator == 1:
                velocity = calculate_speed.differencer(goal_angular, self.angular+360.0)
            elif operator == -1:
                velocity = calculate_speed.differencer(goal_angular, self.angular-360.0)
            else:
                velocity = calculate_speed.differencer(goal_angular, self.angular)
            print(self.angular)
            if velocity == 0:
                print('finish')
                flag = False
            velocity_message = Twist()
            velocity_message.linear.x = 0.0
            velocity_message.angular.z = velocity
            self.pub_vel.publish(velocity_message)


def main():
    rclpy.init()
    executor = MultiThreadedExecutor()
    node = Control_System()
    executor.add_node(node)
    rclpy.spin()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
