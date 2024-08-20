import rclpy
from rclpy.node import Node
from cam_msg.msg import *        # import all messages from cam_msg
from py_pubsub.assign_values import cam_2_pub

class CAMPublisher(Node): 

    def __init__(self):
        super().__init__('cam_publisher')
        self.publisher_ = self.create_publisher(CAM, 'cam_topic', 200)
        timer_period = 0.5  # seconds 
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
    
    def timer_callback(self):
        self.publisher_.publish(cam_2_pub)
        self.get_logger().info('Publishing: "%s"' % cam_2_pub)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    cam_publisher = CAMPublisher() 

    rclpy.spin(cam_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    cam_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
