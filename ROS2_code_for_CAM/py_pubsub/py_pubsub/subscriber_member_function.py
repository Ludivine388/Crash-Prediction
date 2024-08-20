import rclpy
from rclpy.node import Node
from cam_msg.msg import *        # import all messages from cam_msg
from py_pubsub.assign_values import cam_2_pub


class CAMSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            CAM,                                              
            'cam_topic',
            self.listener_callback,
            10)
        self.subscription

    def listener_callback(self, msg):
            self.get_logger().info('Listening: "%s"' % cam_2_pub)  


def main(args=None):
    rclpy.init(args=args)

    cam_subscriber = CAMSubscriber()

    rclpy.spin(cam_subscriber)

    cam_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
