#!/usr/bin/env python3
# license removed for brevity
import rospy
import rospkg
from sensor_msgs.msg import Image

# Import OpenCV libraries and tools
import cv2
from cv_bridge import CvBridge, CvBridgeError
# Initialize the CvBridge class
bridge = CvBridge()

def feeder():
    pub = rospy.Publisher("/camera/rgb/image_raw", Image, queue_size=5)
    rospy.init_node('opencv_feeder', anonymous=True)
    rate = rospy.Rate(10) # 1hz
    while not rospy.is_shutdown():
        # get array data of the image
        try:
            rospack = rospkg.RosPack()
            image_path = rospack.get_path('turtlebot_dabit') + '/img/' + 'ghost.png'
            img = cv2.imread(image_path, 1)

            cv_image = bridge.cv2_to_imgmsg(img, "passthrough")
        except CvBridgeError as e:
            print(e)

        pub.publish(cv_image)
        rate.sleep()

if __name__ == '__main__':
    try:
        feeder()
    except rospy.ROSInterruptException:
        pass