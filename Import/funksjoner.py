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

import numpy as np
import cv2 as cv
import os
import csv
import math
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report

def getResolution(resolution):   #Ikke noe funskjon per nå, er for å evt ikke skrive inn oppløsning

    switcher = {
        240: (426, 240),
        360: (640, 360),
        480: (853, 480),
        720: (1280, 720),
        1080: (1920, 1080)
    }

    return switcher.get(resolution)


def resize(img, resolution, interpolation):
    """
    Function for resizing an image with a defined resolution and interpolation algorithm.
    :param img: source input image
    :param resolution: dimensions for new image (e.g. (480, 360))
    :param interpolation: INTER_NEAREST – a nearest-neighbor interpolation INTER_LINEAR – a bilinear interpolation (used by default) INTER_AREA – resampling using pixel area relation. It may be a preferred method for image decimation, as it gives moire’-free results. But when the image is zoomed, it is similar to the INTER_NEAREST method. INTER_CUBIC – a bicubic interpolation over 4×4 pixel neighborhood INTER_LANCZOS4 – a Lanczos interpolation over 8×8 pixel neighborhood
    :return: resized image
    """
    img = cv.resize(img, resolution, interpolation=interpolation)

    return img


def bilateralFilter(img, diameter, sigmaColour, sigmaSpace):
    """
    Applies the bilateral filter to an image.
    Diameter size: Large filters (d > 5) are very slow, so it is recommended to use d=5 for real-time applications, and perhaps d=9 for offline applications that need heavy noise filtering.
    Sigma values: For simplicity, you can set the 2 sigma values to be the same. If they are small (< 10), the filter will not have much effect, whereas if they are large (> 150), they will have a very strong effect, making the image look “cartoonish”.
    :param img: Source 8-bit or floating-point, 1-channel or 3-channel image.
    :param diameter: Diameter of each pixel neighborhood that is used during filtering. If it is non-positive, it is computed from sigmaSpace .
    :param sigmaColour:Filter sigma in the color space. A larger value of the parameter means that farther colors within the pixel neighborhood (see sigmaSpace ) will be mixed together, resulting in larger areas of semi-equal color.
    :param sigmaSpace: Filter sigma in the coordinate space. A larger value of the parameter means that farther pixels will influence each other as long as their colors are close enough (see sigmaColor ). When d>0 , it specifies the neighborhood size regardless of sigmaSpace . Otherwise, d is proportional to sigmaSpace .
    :return: Bilaterally blurred image
    """
    img2 = cv.bilateralFilter(img, diameter, sigmaColour, sigmaColour)
    return img2

def gaussianBlur(img, kernelSize, sigmaX, sigmaY):
    """
    Blurs an image using a Gaussian filter.
    :param img: input image; the image can have any number of channels, which are processed independently, but the depth should be CV_8U, CV_16U, CV_16S, CV_32F or CV_64F.
    :param kernelSize: Gaussian kernel size. ksize.width and ksize.height can differ but they both must be positive and odd.
    :param sigmaX: Gaussian kernel standard deviation in X direction.
    :param sigmaY: Gaussian kernel standard deviation in Y direction; if sigmaY is zero, it is set to be equal to sigmaX, if both sigmas are zeros, they are computed from ksize.width and ksize.height , respectively
    :return: Gaussian blurred image
    """
    img2 = cv.GaussianBlur(img, kernelSize, sigmaX, sigmaY)
    return img2

def medianBlur(img, kernelSize):
    """
    Blurs an image using the median filter.
    :param img:  input 1-, 3-, or 4-channel image; when ksize is 3 or 5, the image depth should be CV_8U, CV_16U, or CV_32F, for larger aperture sizes, it can only be CV_8U.
    :param kernelSize:aperture linear size; it must be odd and greater than 1, for example: 3, 5, 7 ..
    :return: Median blurred image
    """
    img2 = cv.medianBlur(img, kernelSize)
    return img2

def backgroundSubtractorKNN(history, dist2Threshold, shadow):
    """
    Function for creating background subtractor with the 'K Nearest Neighbours' method.
    :param history: INT(Default value=150), Number of pixels to be used for background image
    :param dist2Threshold: FLOAT (Default value=400.0), threshold for determining if a pixel is different from the background, lower value is more sensitive.
    :param shadow: BOOL, whether to detect shadows or not.
    :return: Background subtractor KNN object
    """
    subtractor = cv.createBackgroundSubtractorKNN(history, dist2Threshold, detectShadows=shadow)
    return subtractor

def backgroundSubtractorMOG2(history, dist2Threshold, shadow):
    """
    Function for creating background subtractor with the 'MOG2' method.
    :param history: INT(Default value=150), Number of pixels to be used for background image
    :param dist2Threshold: FLOAT (Default value=400.0), threshold for determining if a pixel is different from the background, lower value is more sensitive.
    :param shadow: BOOL, whether to detect shadows or not.
    :return: Background subtractor MOG2 object
    """
    subtractor = cv.createBackgroundSubtractorMOG2(history, dist2Threshold, detectShadows=shadow)
    return subtractor

def connectedComponents(img, connectivityParam, minSize, maxSize):
    """
    Finds connected components in the 8-bit single-channel image, colours them white and colors the rest of the pixels black
    :param img: 8-bit single-channel image
    :param connectivityParam: INT, 8 or 4. Sets 4- or 8-way connectivity
    :return: 8-bit single-channel image with only connected components in white
    """
    # find all your connected components (white blobs in your image)
    nb_components, output, stats, centroids = cv.connectedComponentsWithStats(img, connectivity=connectivityParam, ltype=cv.CV_32S)
    # connectedComponentswithStats yields every seperated component with information on each of them, such as size
    # the following part is just taking out the background which is also considered a component, but most of the time we don't want that.
    sizes = stats[1:, -1];
    nb_components = nb_components - 1

    # minimum size of particles we want to keep (number of pixels)
    # here, it's a fixed value, but you can set it as you want, eg the mean of the sizes or whatever
    #min_size = minSize
    #max_size = maxSize

    # your answer image
    img2 = np.zeros(output.shape)
    # for every component in the image, you keep it only if it's above min_size
    for j in range(0, nb_components):
        if minSize <= sizes[j] <= maxSize:
            img2[output == j + 1] = 255

    return img2



def readFromPath(path, fileType): #copied from https://mkyong.com/python/python-how-to-list-all-files-in-a-directory/
    """
    Rekursiv funksjon som finner alle filer i gitt path som inneholder gitt filending i navnet sitt
    :param path: Relativ eller absolutt path til mappe funksjonen starter i
    :param fileType: String funksjonen finner matcher av i alle filer under gitt path
    :return: Returnerer liste med pather til alle filer som oppfyller gitt kriterie
    """
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if fileType in file:
                files.append(os.path.join(r, file))
    return files


def claheFilter(clipLimitThreshold, tileGridSize):
    """
    Performs a contrast limited adaptive histogram equalization on an image
    :param img: Original image to apply CLAHE filter to, BGR format required
    :param clipLimitThreshold: FLOAT, typical value 2
    :param tileGridSize: (int, int) Size of grid for equalization, typical value (8, 8)

    :return Filtered image in grayscale
    """
    claheFiltrator = cv.createCLAHE(clipLimitThreshold, tileGridSize)
    return claheFiltrator

def jaccardIndexPolygons(Ax1, Ay1, Ax2, Ay2, Bx1, By1, Bx2, By2, Xratio, Yratio):
    """
    Funksjon for å regne ut jaccard index av to polygoner
    :param Ax1: Koordinat X1 for Polygon 1
    :param Ay1: Koordinat Y1 for Polygon 1
    :param Ax2: Koordinat X2 for Polygon 1
    :param Ay2: Koordinat Y2 for Polygon 1
    :param Bx1: Koordinat X1 for Polygon 2
    :param By1: Koordinat Y1 for Polygon 2
    :param Bx2: Bredde på Polygon 2
    :param By2: Høyde på Polygon 2
    :param Xratio: Float, typisk 1-3. Ratio som Polygon 2 skal justeres med i horisontal retning.
    :param Yratio: Float, typisk 1-3. Ratio som Polygon 2 skal justeres med i vertikal retning.
    :return: Float, Jaccard index for de to polygonene.
    """
    Ax1 = int(Ax1)
    Ay1 = int(Ay1)
    Ax2 = int(Ax2 + Ax1)
    Ay2 = int(Ay2 + Ay1)
    polygonA = Polygon([(Ax1, Ay1), (Ax2, Ay1), (Ax2, Ay2), (Ax1, Ay2)])

    Bx1 = int(float(Bx1) / Xratio)
    By1 = int(float(By1) / Yratio)
    Bx2 = int((float(Bx2) / Xratio) + float(Bx1))
    By2 = int((float(By2) / Yratio) + float(By1))
    polygonB = Polygon([(Bx1, By1), (Bx2, By1), (Bx2, By2), (Bx1, By2)])

    intersectionArea = polygonA.intersection(polygonB)
    if (polygonA.area + polygonB.area - intersectionArea.area) > 0.0:
        jaccardIndex = (intersectionArea.area) / (polygonA.area + polygonB.area - intersectionArea.area)
    else:
        jaccardIndex = 0

    return jaccardIndex

def resultatAnalyse(fasitPath, resPath):
    """
    Funksjon for å analysere kvalitet på deteksjoner gjort i forhold til fasitfil.
    :param fasitPath: Relativ eller absolutt path til CSV-fil i modifisert MOT ZIP 1.1-format, hvor førstelinje kun er antall frames i filen
    :param resPath: Relativ eller absolutt path til CSV-fil produsert av TestDeteksjon.py
    :return: Returnerer jaccard index på korrekt detekterte frames og inkorrekt detekterte frames
    """
    #fasitPath = "./Test/Devfile/Dev01ShortRef.csv"
    #resPath = "./Test/Devfile/Dev01ShortRes.csv"

    fasitFil = open(fasitPath)
    fasitReader = csv.reader(fasitFil)

    frameCountTotalLine = next(fasitReader)
    frameCountTotal = int(frameCountTotalLine[0])

    resultatFil = open(resPath)
    resultatReader = csv.reader(resultatFil)
    resPathSplit = resPath.split('/')
    timePassed = next(resultatReader)

    resultResolutionRow = next(resultatReader)
    resultResolutionY = resultResolutionRow[1]
    resultResolutionY = resultResolutionY.replace(')', ' ')
    resultResolutionY = int(resultResolutionY)
    resultResolutionX = resultResolutionRow[0]
    resultResolutionX = resultResolutionX.replace('(', ' ')
    resultResolutionX = int(resultResolutionX)
    XAxisRatio = resultResolutionX / 1280
    YAxisRatio = resultResolutionY / 720

    backgroundSubtractionFrames = next(resultatReader)
    next(resultatReader)

    # List where entries are either 0 or 1, where 1 is considered a correctly detected frame. Index corresponds to the frame number in the video.
    analyseList = []
    i = 0

    # List where entries contain the jaccard index of the best fitting frame from each entry in resultatReader
    jaccardIndexList = []

    # Creates the list of lists, index corresponds to frame numbers, entry 0 is unused
    analyseList = [[] for i in range(frameCountTotal + 1)]


    returnList = []
    returnList.append(0)
    returnList.append([])

    referenceList = []
    testList = []
    for i in range(frameCountTotal + 1):
        referenceList.append(0)
        testList.append(0)

    # Marks every frame in the fasit file as incorrect (0) in analyseList, then appends the X1, Y1, X2, Y2 values to the list that corresponds to the frame number
    for fasitLinje in fasitReader:
        frameNr = int(fasitLinje[0])
        referenceList[frameNr] = 1
        analyseList[frameNr].append(int(float(fasitLinje[2])))
        analyseList[frameNr].append(int(float(fasitLinje[3])))
        analyseList[frameNr].append(int(float(fasitLinje[4])))
        analyseList[frameNr].append(int(float(fasitLinje[5])))

    for resultatLinje in resultatReader:
        frameNr = int(resultatLinje[0])
        if frameNr > frameCountTotal:
            print("Rammetall " + str(frameNr) + " i resultatfilen er ikke dekket av fasitfilen.")
            break
        testList[frameNr] = 1
        if referenceList[frameNr] != 0 and frameNr > int(backgroundSubtractionFrames[0]):
            # Regner ut hvor mange annoteringsbokser det er for rammen
            nrOfFrames = int(len(analyseList[frameNr]))
            i = 0
            bestJaccardScore = 0
            while i < nrOfFrames:
                jaccardScore = jaccardIndexPolygons(analyseList[frameNr][i], analyseList[frameNr][i + 1],
                                                       analyseList[frameNr][i + 2],
                                                       analyseList[frameNr][i + 3], resultatLinje[1], resultatLinje[2],
                                                       resultatLinje[3], resultatLinje[4], XAxisRatio, YAxisRatio)
                if jaccardScore > bestJaccardScore:
                    bestJaccardScore = jaccardScore
                i += 4
            jaccardIndexList.append(bestJaccardScore)
            bestJaccardScore = 0




    #fig1, ax1 = plt.subplots()
    #ax1.set_title(fasitPath)
    #ax1.boxplot(jaccardIndexList)
    #plt.savefig(fasitPath + 'boxplot.png', bbox_inches='tight')

    labelString = str(resPathSplit[3] + ":")

    returnList[0] = labelString

    for val in jaccardIndexList:
        returnList[1] = jaccardIndexList

    return returnList, referenceList, testList

def multifilResultatAnalyseUtvikling(folderName):
    folderPath = str("./Test/" + folderName + "/")
    fasitPathStub = "./Fasitfiler/DevSet/"

    #analysePath = folderPath + "/analyse.txt"
    #analyseFil = open(analysePath, "w+")
    confusion_matrix_file = open(str(folderPath + "confusion_matrix.txt"), "w+")

    plotList = []
    confusion_matrix_list = []

    resFiles = readFromPath(folderPath, ".csv")
    for resFile in resFiles:
        resSplit = resFile.split('/')
        fasitPath = str(fasitPathStub + resSplit[3])
        bestJacFit, referenceList, predictedList = resultatAnalyse(fasitPath, resFile)
        confusion_matrixes = confusion_matrix(referenceList, predictedList)
        confusion_matrixes_normalized = confusion_matrix(referenceList, predictedList, normalize='true')
        confusion_matrixes_report = (classification_report(referenceList, predictedList))
        confusion_matrix_file.write(resFile + "\n" + str(confusion_matrixes) + "\n" + str(confusion_matrixes_normalized)
                                    + "\n" + str(confusion_matrixes_report) + "\n")
        plotList.append(bestJacFit)
    confusion_matrix_file.close()

    plotListIterator = iter(plotList)
    figs, axes = plt.subplots(2, 4, sharey=True)

    for i, row in enumerate(axes):
        for j, col in enumerate(row):
            pltList = next(plotListIterator)
            pltListName = str(pltList[0]).split('.')
            axes[i, j].boxplot(pltList[1])
            axes[i, j].set_xticks([])
            axes[i, j].set_title(str(pltList[0]), fontsize=6)



    plt.savefig(folderPath + "statistics.png", bbox_inches='tight')

    return

def multifilResultatAnalyseTest(folderName):
    folderPath = str("./Test/" + folderName + "/")
    fasitPathStub = "./Fasitfiler/Testset/"

    #analysePath = folderPath + "/analyse.txt"
    #analyseFil = open(analysePath, "w+")

    confusion_matrix_file = open(str(folderPath + "confusion_matrix.txt"), "w+")

    plotList = []
    confusion_matrix_list = []

    resFiles = readFromPath(folderPath, ".csv")

    for resFile in resFiles:
        resSplit = resFile.split('/')
        fasitPath = str(fasitPathStub + resSplit[3])
        bestJacFit, referenceList, predictedList = resultatAnalyse(fasitPath, resFile)
        confusion_matrixes = confusion_matrix(referenceList, predictedList)
        confusion_matrixes_normalized = confusion_matrix(referenceList, predictedList, normalize='true')
        confusion_matrixes_report = (classification_report(referenceList, predictedList))
        confusion_matrix_file.write(resFile + "\n" + str(confusion_matrixes) + "\n" + str(confusion_matrixes_normalized)
                                    + "\n" + str(confusion_matrixes_report) + "\n")
        plotList.append(bestJacFit)
    confusion_matrix_file.close()

    plotListIterator = iter(plotList)
    figs, axes = plt.subplots(5, 4, sharey=True)

    #Making each subplot
    for i, axs in enumerate(axes):
        for j, col in enumerate(axs):
            pltList = next(plotListIterator)
            pltListName = str(pltList[0]).split('.')
            axes[i, j].boxplot(pltList[1])
            axes[i, j].set_xticks([])
            axes[i, j].set_title(str(pltListName[0]), fontsize=5)

    plt.subplots_adjust(hspace=0.25, wspace=0.25)
    plt.savefig(folderPath + "statistics.png", bbox_inches='tight')
