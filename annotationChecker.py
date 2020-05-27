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

import cv2 as cv
import sys
import os
import csv
sys.path.append('./Import') #For å importene funksjoner så må vi bytte mappe
import funksjoner as fu

videoFile = "./Data/File1-[2017-08-28 14-56-15]-080-1.m4v"
cap = cv.VideoCapture(videoFile)

annotationFilePath = "./Fasitfiler/Cvat-outsource/CVAT 2/File1-[2017-08-28 14-56-15]-080-1.m4v.csv"
annotationFile = open(annotationFilePath)
annotationReader = csv.reader(annotationFile)
#next(annotationReader)
annotationLine = next(annotationReader)

Res = fu.getResolution(720)
interpolation = cv.INTER_LANCZOS4

while True:
    ret, frame = cap.read()
    if frame is None:
        break
    if frame is None:
        break
    frameNr = cap.get(cv.CAP_PROP_POS_FRAMES)

    if int(frameNr) == int(annotationLine[0]):
        x1 = int(float(annotationLine[2]))
        y1 = int(float(annotationLine[3]))
        x2 = x1 + int(float(annotationLine[4]))
        y2 = y1 + int(float(annotationLine[5]))
        frame = cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
        try:
            annotationLine = next(annotationReader)
        except StopIteration:
            print("End of annotation file")
    elif int(frameNr) > int(annotationLine[0]):
        try:
            annotationLine = next(annotationReader)
        except StopIteration:
            print("End of annotation file")

    frame = fu.resize(frame, Res, interpolation)
    cv.imshow("Original", frame)

    keyboard = cv.waitKey(1)
    if keyboard == 'q' or keyboard == 27:
        break

cap.release()
cv.waitKey(1)
cv.destroyAllWindows()
for i in range(1, 5):
    cv.waitKey(1)
