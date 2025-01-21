import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from message_filters import Subscriber, ApproximateTimeSynchronizer

class Panorama(Node):

    def __init__(self):
        super().__init__("pano_node")
        self.get_logger().info("Hello Abyss Solutions")
        self.sub1 = Subscriber(self, Image, '/platypus/camera_1/dec/manual_white_balance')
        self.sub2 = Subscriber(self, Image, '/platypus/camera_2/dec/manual_white_balance')
        self.sub3 = Subscriber(self, Image, '/platypus/camera_3/dec/manual_white_balance')

        self.cv_bridge = CvBridge()
        self.synchronizer = ApproximateTimeSynchronizer([self.sub1, self.sub2, self.sub3], 10, 1)
        self.synchronizer.registerCallback(self.image_callback)

    def image_callback(self, img1, img2, img3):
        self.get_logger().info("Received image")
        # try:
        #     cv_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        #     cv2.imshow('Middle Camera', cv_image)
        #     cv2.waitKey(1)
        # except Exception as e:
        #     self.get_logger().error('Could not convert image: {}'.format(e))

    
def main(args=None):
    rclpy.init(args=args)
    node = Panorama()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()