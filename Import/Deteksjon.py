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

#!/usr/bin/python

import numpy as np
import cv2 as cv
from time import perf_counter
import sys
import datetime
import os

from Import import funksjoner as fu


def testing(datasett, modus, devMode, eksporter_path):
    print("Testing er valgt")
    print("Datasett: " + datasett)
    print("Modus: " + modus)

    if datasett == "Testsett": #Testsett er valgt
        filenames = fu.readFromPath("./Data/Test/", ".mp4")
        main(filenames, modus, devMode, eksporter_path, datasett)

    elif datasett == "Utviklingssett":
        filenames = fu.readFromPath("./Data/Utvikling/", ".m4v")
        main(filenames, modus, devMode, eksporter_path, datasett)

    else:
        print("This message should never appear.")


def path(filenames, modus, devMode, eksporter_path):
    main(filenames, modus, devMode, eksporter_path)


def main(filenames, modus, devMode, eksporter_path, datasett=""):

    #####   Creates folder for result files #####
    datetimeTid = str(datetime.datetime.now().isoformat())
    datetimePath = datetimeTid.replace(":", "_")

    ### Output for konsoll angående resultatmappe ###
    if eksporter_path != "":
        print("Resultatmappe: " + eksporter_path)
    else:
        print("Ingen resultatmappe er valgt, default er 'Test'")


    if modus == "Hurtig": #Hurtig modus er valgt
        Res = fu.getResolution(360)
        interpolation = cv.INTER_LANCZOS4

        BGShistory = 100
        BGSubtractor = fu.backgroundSubtractorKNN(BGShistory, 30.0, False)

        kernel = cv.getStructuringElement(cv.MORPH_OPEN, (3, 3))

        minSize = 1000
        maxSize = float('inf')
        connectivity = 8

    elif modus == "Sakte": #Sakte modus er valgt

        Res = fu.getResolution(360)
        interpolation = cv.INTER_LANCZOS4

        BGShistory = 150
        BGSubtractor = fu.backgroundSubtractorKNN(BGShistory, 30.0, False)

        kernel = cv.getStructuringElement(cv.MORPH_OPEN, (3, 3))

        minSize = 1000
        maxSize = float('inf')
        connectivity = 8

    else:
        print("Her har det skjedd noe feil..") #Meldingen skal ikke printes, da har det skjedd noe feil..

    #Starts test timer
    test_starttime = perf_counter()

    # Global values
    i = 0


    arr = []


    ### Definere filer som skal kjøres ###
    if datasett != "":
        arr = filenames  # Om datasett er valgt, så erstatter filanames, arr.
    else:
        for file in filenames: #Legger inn files i arr for å slippe problemet med at en liste ikke vil leses
            arr += file



    #Globale verdier
    videoCount = 0
    totaltAntall = 0

    j = 0

    ### Checking if Export path has been choosen, if not then defult ###
    if eksporter_path != "":
        os.mkdir(str(eksporter_path + '/' + datetimePath))
    else:
        os.mkdir(str("./Test/" + datetimePath))


    #####   MAIN STARTS HERE    #####
    for file in arr:
        file_start = perf_counter()
        cap = cv.VideoCapture(file)
        file = file.replace('.mp4', '') #Fjerner .mp4 ending

        # Konsoll output som ser ryddig ut

        if totaltAntall == 0:
            totaltAntall = len(arr)
            print("Totalt antall filer: " + str(totaltAntall))
            print("\n")
        print("Aktiv fil: " + file)

        statFilPath = (str(file + ".txt"))
        frameList = []



        while True:
            ret, frame = cap.read()
            if frame is None:
                break

            #####   Pre-processing  -   Resizing    #####
            frame = fu.resize(frame, Res, interpolation)  # Resize av frame med definert oppløsning
            if devMode == True: #Om Utviklingsmodus er aktivert, så vises imshow
                cv.imshow(file, frame)


            #####   Background subtraction  #####
            frame = BGSubtractor.apply(frame)
            if devMode == True:  # Om Utviklingsmodus er aktivert, så vises imshow
                cv.imshow('Post-BGSubtraction', frame)

            #####   Morphology  #####
            frame = cv.morphologyEx(frame, cv.MORPH_OPEN, kernel, iterations=1)
            #frame = cv.morphologyEx(frame, cv.MORPH_CLOSE, kernel, iterations=2)  # kan legge til iterations her
            if devMode == True:  # Om Utviklingsmodus er aktivert, så vises imshow
                cv.imshow('Post-Morph', frame)


            #####   Connected components    #####
            frame = fu.connectedComponents(frame, connectivity, minSize, maxSize)
            frame = np.uint8(frame)
            if devMode == True:  # Om Utviklingsmodus er aktivert, så vises imshow
                cv.imshow('Post-connectedComponents', frame)

            #####   Finding contours    #####
            contours, hierarchy = cv.findContours(frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

            frame = cv.cvtColor(frame, cv.COLOR_GRAY2RGB)

            for contour in contours:
                if 200 <= cv.contourArea(contour) <= 100000:

                    (x, y, w, h) = cv.boundingRect(contour)
                    # making green rectangle around the moving object
                    frame = cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    
                    
                    #Adds frame number if there is a detected contour to frameList
                    detected_frame_number = 0
                    detected_frame_number = cap.get(cv.CAP_PROP_POS_FRAMES)
                    found_frame_string = str(str(int(detected_frame_number)) + "," + str(x) + "," + str(y) + "," + str(w) +"," + str(h))
                    frameList.append(found_frame_string)

                    # Antall fisk
                    i += 1

            if devMode == True:  # Om Utviklingsmodus er aktivert, så vises imshow
                cv.imshow('Post-Detected contours', frame)

            keyboard = cv.waitKey(1)
            if keyboard == 'q' or keyboard == 27:
                break

        cap.release()
        cv.waitKey(1)
        cv.destroyAllWindows()

        videoCount += 1
        antallGjenstaaende = totaltAntall - videoCount


        if antallGjenstaaende != 0:
            print("Antall fullført vidoer: " + str(videoCount))
            print("Antall videoer som gjenstår: " + str(antallGjenstaaende))
        else:
            print("Alle videoer er fullført")



        print("\n")

        for i in range(1, 5):
            cv.waitKey(1)



        #####   WRITING FRAMES TO FILE  #####
        fileStringSplit = file.split('/')

        ### Checking if Export path has been choosen, if not then defult ###
        if eksporter_path != "":
            file = str(eksporter_path + '/' + datetimePath + '/' + fileStringSplit[-1])
        else:
            file = str('./Test/' + datetimePath + '/' + fileStringSplit[-1])

        file = file.replace('.m4v', '.csv')  # Fjerner .mp4 ending
        file = file.replace('.mp4', '.csv')


        statFil = open(file, "w+")

        for frame in frameList:
            statFil.write("\n")
            statFil.write(str(frame))

        frameList.clear()


        #Ends file timer and prints result
        time_passed_file = perf_counter() - file_start  # Stops test timer after writing to file
        statFil.seek(0, 0)
        statFil.write(str(time_passed_file))
        statFil.write("\n")
        statFil.write(str(Res))
        statFil.write("\n")
        statFil.write(str(BGShistory))
        statFil.write("\n")
        statFil.close()

    if datasett == "Utviklingssett":
        fu.multifilResultatAnalyseUtvikling(datetimePath)

    elif datasett == "Testsett":
        fu.multifilResultatAnalyseTest(datetimePath)
            
    #Ends test timer and prints result
    total_time_elapsed = perf_counter() - test_starttime
    print('Total test time:', total_time_elapsed)

