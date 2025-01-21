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
        self.cv_bridge = CvBridge()

    def image_callback(self, msg):
        self.get_logger().info("Received image")
        try:
            cv_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            cv2.imshow('Middle Camera', cv_image)
            cv2.waitKey(1)
        except Exception as e:
            self.get_logger().error('Could not convert image: {}'.format(e))


def main(args=None):
    rclpy.init(args=args)
    node = Panorama()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()