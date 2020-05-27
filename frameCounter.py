#####
#This file is part of 'DAF-Bachelorprosjekt 2020'.
#
#'DAF-Bachelorprosjekt 2020' is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#'DAF-Bachelorprosjekt 2020' is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with 'DAF-Bachelorprosjekt 2020'.  If not, see https://www.gnu.org/licenses/.
#####

import cv2

def count_frames_manual(video):
    # initialize the total number of frames read
    total = 0
    # loop over the frames of the video
    while True:
        # grab the current frame
        (grabbed, frame) = video.read()

        # check to see if we have reached the end of the
        # video
        if not grabbed:
            break
        # increment the total number of frames read
        total += 1
    # return the total number of frames in the video file
    return total

path = "./Data/Test/File1-[2017-08-28_14-56-15]-056.mp4"
video = cv2.VideoCapture(path)
print(count_frames_manual(video))
