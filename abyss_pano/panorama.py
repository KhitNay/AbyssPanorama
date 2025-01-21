import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class Panorama(Node):

    def __init__(self):
        super().__init__("pano_node")
        self.get_logger().info("Hello Abyss Solutions")
        self.subscriber = self.create_subscription(Image,
                                                   '/platypus/camera_2/dec/manual_white_balance',
                                                   self.image_callback,
                                                   10)

    def image_callback(self, msg):
        self.get_logger().info("Image received from camera 2")


def main(args=None):
    rclpy.init(args=args)
    node = Panorama()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()