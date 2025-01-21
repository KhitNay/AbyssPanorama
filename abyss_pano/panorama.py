import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from message_filters import Subscriber, ApproximateTimeSynchronizer

class Panorama(Node):
    def __init__(self):
        super().__init__("pano_node")
        self.sub1 = Subscriber(self, Image, '/platypus/camera_1/dec/manual_white_balance')
        self.sub2 = Subscriber(self, Image, '/platypus/camera_2/dec/manual_white_balance')
        self.sub3 = Subscriber(self, Image, '/platypus/camera_3/dec/manual_white_balance')

        self.cv_bridge = CvBridge()
        self.synchronizer = ApproximateTimeSynchronizer([self.sub1, self.sub2, self.sub3], 10, 0.1)
        self.synchronizer.registerCallback(self.image_callback)

    def image_callback(self, img1, img2, img3):
        try:
            cv_image1 = self.cv_bridge.imgmsg_to_cv2(img1, desired_encoding='bgr8')
            cv_image2 = self.cv_bridge.imgmsg_to_cv2(img2, desired_encoding='bgr8')
            cv_image3 = self.cv_bridge.imgmsg_to_cv2(img3, desired_encoding='bgr8')

            images = [cv_image1, cv_image2, cv_image3]
            panorama = self.create_panorama(images)

            if panorama is not None:
                cv2.imshow("Panorama", panorama)
                cv2.waitKey(1)

        except Exception as e:
            self.get_logger().error(f"Could not process images: {e}")

    def create_panorama(self, images):
        try:
            stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
            status, panorama = stitcher.stitch(images)

            if status == cv2.Stitcher_OK:
                self.get_logger().info("Successfully created panorama")
                return panorama
            else:
                self.get_logger().error("Stitching failed. Errror code: {}".format(status))
            return None
        except Exception as e:
            self.get_logger().error("Stitching failed. Exception: {}".format(status))
            return None


def main(args=None):
    rclpy.init(args=args)
    node = Panorama()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
