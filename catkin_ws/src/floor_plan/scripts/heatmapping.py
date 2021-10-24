'''  
Copyright (c) 2017 Intel Corporation.
Licensed under the MIT license. See LICENSE file in the project root for full license information.
'''
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
import copy
import rospy

# Initialize the ROS Node named 'opencv_example', allow multiple nodes to be run with this name
rospy.init_node('heat_mapper_live', anonymous=True)

def main():
    resource = 3
    cap = cv2.VideoCapture(resource)
    if not cap.isOpened():
        rospy.loginfot("Error opening resource: " + str(resource))
        exit(0)
    else:
        rospy.loginfo("video loaded")
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

    # number of frames is a variable for development purposes, you can change the for loop to a while(cap.isOpened()) instead to go through the whole video
    num_frames = 1000

    first_iteration_indicator = 1
    for i in range(0, num_frames):
        '''
        There are some important reasons this if statement exists:
            -in the first run there is no previous frame, so this accounts for that
            -the first frame is saved to be used for the overlay after the accumulation has occurred
            -the height and width of the video are used to create an empty image for accumulation (accum_image)
        '''
        if (first_iteration_indicator == 1):
            ret, frame = cap.read()
            first_frame = copy.deepcopy(frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            height, width = gray.shape[:2]
            accum_image = np.zeros((height, width), np.uint8)
            first_iteration_indicator = 0
        else:
            ret, frame = cap.read()  # read a frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to grayscale

            fgmask = fgbg.apply(gray)  # remove the background

            # for testing purposes, show the result of the background subtraction
            # cv2.imshow('diff-bkgnd-frame', fgmask)

            # apply a binary threshold only keeping pixels above thresh and setting the result to maxValue.  If you want
            # motion to be picked up more, increase the value of maxValue.  To pick up the least amount of motion over time, set maxValue = 1
            thresh = 2
            maxValue = 2
            ret, th1 = cv2.threshold(fgmask, thresh, maxValue, cv2.THRESH_BINARY)
            # for testing purposes, show the threshold image
            # cv2.imwrite('diff-th1.jpg', th1)

            # add to the accumulated image
            accum_image = cv2.add(accum_image, th1)
            # for testing purposes, show the accumulated image
            # cv2.imwrite('diff-accum.jpg', accum_image)

            # for testing purposes, control frame by frame
            # raw_input("press any key to continue")

            # for testing purposes, show the current frame
            # cv2.imshow('frame', gray)

        # apply a color map
        # COLORMAP_PINK also works well, COLORMAP_BONE is acceptable if the background is dark
        color_image = im_color = cv2.applyColorMap(accum_image, cv2.COLORMAP_HOT)
        # for testing purposes, show the colorMap image
        # cv2.imwrite('diff-color.jpg', color_image)

        # overlay the color mapped image to the first frame
        result_overlay = cv2.addWeighted(first_frame, 0.7, color_image, 0.7, 0)

        # save the final overlay image
        cv2.imshow('images/diff-overlay.jpg', result_overlay)
        
        # Loop to keep the program from shutting down unless ROS is shut down, or CTRL+C is pressed
        while not rospy.is_shutdown():
            rospy.spin()

#---

#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_video_resource.py contains
a testing code to see if opencv can open a video stream
useful to debug if video_stream does not work
"""

# import cv2
# import sys

# if __name__ == '__main__':
#     if len(sys.argv) < 2:
#         print("You must give an argument to open a video stream.")
#         print("  It can be a number as video device, e.g.: 0 would be /dev/video0")
#         print("  It can be a url of a stream,        e.g.: rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov")
#         print("  It can be a video file,             e.g.: myvideo.mkv")
#         exit(0)

#     resource = sys.argv[1]
#     # If we are given just a number, interpret it as a video device
#     if len(resource) < 3:
#         resource_name = "/dev/video" + resource
#         resource = int(resource)
#     else:
#         resource_name = resource
#     print("Trying to open resource: ", resource_name)
#     cap = cv2.VideoCapture(resource)
#     if not cap.isOpened():
#         print("Error opening resource: " + str(resource))
#         print("Maybe opencv VideoCapture can't open it")
#         exit(0)

#     print("Correctly opened resource, starting to show feed.")
#     rval, frame = cap.read()
#     while rval:
#         cv2.imshow("Stream: " + resource_name, frame)
#         rval, frame = cap.read()
#         key = cv2.waitKey(20)
#         # print "key pressed: " + str(key)
#         # exit on ESC, you may want to uncomment the print to know which key is ESC for you
#         if key == 27 or key == 1048603:
#             break
#     cv2.destroyWindow("preview")