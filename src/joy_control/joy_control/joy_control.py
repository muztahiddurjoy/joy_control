import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist


def map_value(value):
    if value < -1 or value > 1:
        raise ValueError("Input value should be in the range [-1, 1]")
    mapped_value = int(((value + 1) / 2) * 255)
    return mapped_value



class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self._logger.info('Mongoltori is ready to take joystick command')
        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.listener_callback,
            10)
        self.subscription
        self.publishers_ = self.create_publisher(Twist, 'mt_cmd_vel', 10)

    def listener_callback(self, msg):
        rover_msg = Twist()
        x_axis = msg.axes[2]
        y_axis = msg.axes[1]
        base_threshold = map_value(msg.axes[3])
        linear_threshold = base_threshold
        angular_threshold = int(base_threshold/5)
        clutch = msg.buttons[0]

        if(clutch == 1):
            if(y_axis > 0.99):
                rover_msg.linear.x = float(linear_threshold)
                self.get_logger().info('Rover should forward')
            elif (y_axis < -0.99):
                rover_msg.linear.x = float(-linear_threshold)
                self.get_logger().info('Rover should backward')
            else:
                rover_msg.linear.x = 0.0
            
            if(x_axis > 0.99):
                rover_msg.angular.z = float(angular_threshold)
                self.get_logger().info('Rover should turn right')
            elif(x_axis < -0.99):
                rover_msg.angular.z = float(-angular_threshold)
                self.get_logger().info('Rover should turn left')
            else:
                rover_msg.angular.z = 0.0
        else:
            rover_msg.linear.x = 0.0
            rover_msg.angular.z = 0.0

        self.publishers_.publish(rover_msg)

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()