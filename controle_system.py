import math
import os

from geometry_msgs.msg import Twist

from modules import calculate_speed

from nav_msgs.msg import Odometry

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data


class Control_System(Node):
    def __init__(self):
        super().__init__('Control_System')

        self.create_subscription(
            String,
            'control_system/command',
            self.cmmand_callback,
            qos_profile_sensor_data
        )

        self.create_subscription(
            Odometry,
            'odom',
            self.now_angular,
            qos_profile_sensor_data
        )

        self.pub_vel = self.create_publisher(
            Twist,
            'cmd_vel',
            qos_profile_sensor_data
        )

    def now_angular(self, massage):
        self.angular = math.degrees(
            2*math.asin(massage.pose.pose.orientation.z))

    def command_callback(self, msg):

        self.command = msg.data
        command = msg.data.split(',')

        if 'rotate' == command[0].replace('Command:', ''):
            self.rotate(command[1].replace('Content:', ''))

    def cerebrum_publisher(self, message):
        self.senses_publisher = self.create_publisher(
            String, 'cerebrum/command', qos_profile_sensor_data)

        _trans_message = String()
        _trans_message.data = message

        self.senses_publisher.publish(_trans_message)
        self.destroy_publisher(self.senses_publisher)

    def rotate(self, angular):
        angular = int(angular)
        _acceleration = 0
        _velocity = 0

        difference, direction = calculate_speed.space_time_convert(angular)

        flag = 1

        while flag == 1:
            _velocity,
            _acceleration,
            flag = calculate_speed.calculate_next(
                difference,
                direction,
                _velocity,
                _acceleration
            )
            vel = Twist()
            vel.linear.x = 0
            vel.angular.z = _velocity*direction
            self.pub_vel.publish(vel)
        self.cerebrum_publisher('Return:1,Content:None')


def main():
    rclpy.init()
    node = Control_System()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
