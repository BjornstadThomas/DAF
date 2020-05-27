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


### Importering av nødvendige pakker ###
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout \
    , QPushButton, QLabel, QFileDialog, QTableWidget, QTableWidgetItem \
    , QDesktopWidget, QCheckBox, QGroupBox, QMessageBox, QRadioButton

from moviepy.video.io.VideoFileClip import VideoFileClip

import os
import numpy as np
import sys

### Importering av nødvendige moduler ###
from Import import Deteksjon


### Vindu 1 - Innlesing ###
class UI_Innlesing(object):
    def setupUI(self, MainWindow):

        # Oppløsning til skjermen, benyttes for å få korrekt ratio for layout
        screen_shape = QDesktopWidget().screenGeometry()  # Finner oppløsnigen til skjermen
        width = screen_shape.width()
        height = screen_shape.height()

        self.centralwidget = QWidget(MainWindow)

        ### DAF akronym og tekst ###
        self.daf_kort = QLabel('DAF')
        self.daf_kort.setStyleSheet('font-size: 25pt; font-family: Open Sans; border: 0px solid;')
        self.daf_lang = QLabel('Deteksjon av Fisk i Video')  # Label som skal være DAF logo/tekst
        self.daf_lang.setStyleSheet('font-size: 18pt; font-family: Open Sans; border: 0px solid;')

        ### Knapp utformet som ikon for brukerguiden ###
        self.hjelp = QPushButton('')
        self.hjelp.setIconSize(QSize(width * 0.1, height * 0.1))
        self.hjelp.setStyleSheet('QPushButton{border: 0px solid;}')
        self.hjelp.setIcon(QIcon("Vedlegg/Help.png")) # Benytter ikonet "Hjelp.png" fra mappen med Vedlegg

        ### Knapp utformet som ikon for innlesing av filer ###
        self.innlesing_knapp = QPushButton('')
        self.innlesing_knapp.setSizePolicy(int(width * 0.3), int(height * 0.3))
        self.innlesing_knapp.setIconSize(QSize(int(width * 0.3), int(height * 0.3)))
        self.innlesing_knapp.setStyleSheet('QPushButton{border: 0px solid;}') # Endrer stilen til knappen
        self.innlesing_knapp.setIcon(QIcon("Vedlegg/Folder.png"))

        ### Tom Label under Innlesing-ikonet ###
        self.info = QLabel('')  # Label med tekst som beskriver handlingen til mappen
        self.info.setSizePolicy(10, 10)
        self.info.setStyleSheet('font-size: 12pt; font-family: Open Sans; border: 0px solid;')


        ### LAYOUT - UI_Innlesing ###

        ### Layout for Logo ###
        logo_layout = QVBoxLayout() #Vertikalt layout
        logo_layout.addWidget(self.daf_kort, alignment=Qt.AlignRight) # Endrer posisjonering til å være til høyre
        logo_layout.addWidget(self.daf_lang)
        logo_layout.setAlignment(Qt.AlignRight)

        ### Box som grupper Layout til Logo ###
        logo_box = QGroupBox("")  # Logo + Overskrift
        logo_box.setLayout(logo_layout)
        logo_box.setAlignment(Qt.AlignRight)

        ### Layout for Brukerguiden ###
        hjelp_layout = QVBoxLayout() # Vertikalt layout
        hjelp_layout.addWidget(self.hjelp, alignment=Qt.AlignHCenter)

        ### Box som grupper Layout til Brukerguiden ###
        hjelp_box = QGroupBox("")
        hjelp_box.setLayout(hjelp_layout)
        hjelp_box.setMaximumWidth(int(width * 0.125))
        hjelp_box.setAlignment(Qt.AlignLeft)

        ### Layout for Innlesing-knappen ###
        button_layout = QVBoxLayout() # Vertikalt layout
        button_layout.addWidget(self.innlesing_knapp, alignment=Qt.AlignHCenter)
        button_layout.addWidget(self.info)

        ### Box som grupper Layout til Innlesing-knappen ###
        button_box = QGroupBox()
        button_box.setLayout(button_layout)

        ### Overordnet Layout for Innlesing ###
        innlesing_layout = QVBoxLayout() # Vertikalt layout
        innlesing_layout.addWidget(button_box)

        ### Overordnet Layout for Logo og Brukerguiden ###
        head_layout = QHBoxLayout() # Horisontalt layout
        head_layout.addWidget(hjelp_box)
        head_layout.addWidget(logo_box)

        ### Grupperende layout som inkluderer de øvrige layoutene ###
        main_layout = QVBoxLayout() # Vertikalt layout
        main_layout.setAlignment(Qt.AlignLeading)
        main_layout.addLayout(head_layout)
        main_layout.addLayout(innlesing_layout)

        ### Setter CentralWidget sitt Layout til main_layout ###
        self.centralwidget.setLayout(main_layout)

        ### Endrer CentralWidget til MainWindow til å benytte UI_Innlesing sin CentralWidget ###
        MainWindow.setCentralWidget(self.centralwidget)


### Vindu 2 - Valgte Filer ###
class UI_Valgte_Filer(object):
    def setupUI(self, MainWindow):

        # Oppløsning til skjermen, benyttes for å få korrekt ratio for layout
        screen_shape = QDesktopWidget().screenGeometry()  # Finner oppløsningen til skjermen
        width = screen_shape.width()
        height = screen_shape.height()

        self.centralwidget = QWidget(MainWindow)

        self.daf_kort = QLabel('DAF')  # Label som skal være DAF logo/tekst
        self.daf_kort.setStyleSheet('font-size: 25pt; font-family: Open Sans; border: 0px solid;')

        self.daf_lang = QLabel('Deteksjon av Fisk i Video')  # Label som skal være DAF logo/tekst
        self.daf_lang.setStyleSheet('font-size: 18pt; font-family: Open Sans; border: 0px solid;')

        self.hjelp = QPushButton('')  # Hjelp knapp for å vise Brukerguide
        self.hjelp.setIconSize(QSize(width * 0.1, height * 0.1))
        self.hjelp.setStyleSheet('QPushButton{border: 0px solid;}')
        self.hjelp.setIcon(QIcon("Vedlegg/Help.png"))

        self.tabell = QTableWidget()
        self.tabell.setRowCount(0)
        self.tabell.setColumnCount(3)
        self.tabell.setColumnWidth(0, width * 0.45)
        self.tabell.setHorizontalHeaderLabels(["Filnavn", "Filstørrelse", "Lengde"])

        self.legg_til_fil = QPushButton('Legg til fil')
        self.legg_til_fil.setStyleSheet('font-size: 16pt; font-family: Open Sans;')

        ### MODUS (Hurtig / Sakte) ###
        self.modus = QLabel('Modus')
        self.modus.setStyleSheet('font-size: 16pt; font-family: Open Sans; border: 0px solid;')

        UI_Valgte_Filer.hurtig = QRadioButton('Hurtig')
        UI_Valgte_Filer.hurtig.setStyleSheet('font-size: 12pt; font-family: Open Sans; border: 0px solid;')

        UI_Valgte_Filer.sakte = QRadioButton('Sakte')
        UI_Valgte_Filer.sakte.setStyleSheet('font-size: 12pt; font-family: Open Sans; border: 0px solid;')

        ### DEVMODE ###
        self.devMode = QLabel('Utviklingsmodus')
        self.devMode.setStyleSheet('font-size: 16pt; font-family: Open Sans; border: 0px solid;')

        UI_Valgte_Filer.devMode = QCheckBox('Aktiver')
        UI_Valgte_Filer.devMode.setStyleSheet('font-size: 12pt; font-family: Open Sans; border: 0px solid;')

        ### TESTING ###
        self.testing = QLabel('Testing')
        self.testing.setStyleSheet('font-size: 16pt; font-family: Open Sans; border: 0px solid;')

        UI_Valgte_Filer.testing_test = QRadioButton('Testsett')
        UI_Valgte_Filer.testing_test.setStyleSheet('font-size: 12pt; font-family: Open Sans; border: 0px solid;')

        UI_Valgte_Filer.testing_utvikling = QRadioButton('Utviklingssett')
        UI_Valgte_Filer.testing_utvikling.setStyleSheet('font-size: 12pt; font-family: Open Sans; border: 0px solid;')

        UI_Valgte_Filer.kjorTesting = QPushButton('Kjør testing')
        UI_Valgte_Filer.kjorTesting.setStyleSheet('font-size: 16pt; font-family: Open Sans;')

        ### KNAPPER ###
        self.kjorDeteksjon = QPushButton('Kjør deteksjon')
        self.kjorDeteksjon.setStyleSheet('font-size: 16pt; font-family: Open Sans; background-color: #006CD0; color: #ffffff')

        self.tilbake = QPushButton('Tilbake')
        self.tilbake.setStyleSheet('font-size: 16pt; font-family: Open Sans;')

        self.eksporter = QPushButton('Eksporter')
        self.eksporter.setStyleSheet('font-size: 16pt; font-family: Open Sans;')

        ### LAYOUT - UI_Valgte_Filer ###

        ### Layout for Logo ###
        logo_layout = QVBoxLayout()  # Vertikalt layout
        logo_layout.addWidget(self.daf_kort, alignment=Qt.AlignRight)  # Endrer posisjonering til å være til høyre
        logo_layout.addWidget(self.daf_lang)
        logo_layout.setAlignment(Qt.AlignRight)

        ### Box som grupper Layout til Logo ###
        logo_box = QGroupBox("")  # Logo + Overskrift
        logo_box.setLayout(logo_layout)
        logo_box.setAlignment(Qt.AlignRight)

        ### Layout for Brukerguiden ###
        hjelp_layout = QVBoxLayout()
        hjelp_layout.addWidget(self.hjelp, alignment=Qt.AlignHCenter)

        ### Box som grupper Layout til Brukerguiden ###
        hjelp_box = QGroupBox("") #Hjelp knapp
        hjelp_box.setLayout(hjelp_layout)
        hjelp_box.setMaximumWidth(width * 0.125)
        hjelp_box.setAlignment(Qt.AlignLeft)

        ### Layout for Tabellen ###
        tabell_layout = QVBoxLayout()
        tabell_layout.addWidget(self.tabell)

        ### Box som grupper Layout til tabellen ###
        tabell_box = QGroupBox("Filer")  # Tabell med filer
        tabell_box.setLayout(tabell_layout)
        tabell_box.setAlignment(Qt.AlignLeft)

        ### Layout for Modus-knapper ###
        modus_layout = QHBoxLayout()
        modus_layout.addWidget(UI_Valgte_Filer.hurtig)
        modus_layout.addWidget(UI_Valgte_Filer.sakte)

        ### Box som grupper Layout til Modus-knappene ###
        modus_box = QGroupBox('Modus')  # Modus
        modus_box.setLayout(modus_layout)
        modus_box.setAlignment(Qt.AlignTop)

        ### Layout for Utviklingsmodus ###
        devMode_layout = QHBoxLayout()
        devMode_layout.addWidget(UI_Valgte_Filer.devMode)

        ### Box som grupper Layout til Utviklingsmodus ###
        dev_box = QGroupBox('Utviklingsmodus')  # DevMode (imshow eller ikke)
        dev_box.setLayout(devMode_layout)
        dev_box.setAlignment(Qt.AlignTop)

        ### Layout for Testing-knappene ###
        testing_layout = QHBoxLayout()
        testing_layout.addWidget(UI_Valgte_Filer.testing_test)
        testing_layout.addWidget(UI_Valgte_Filer.testing_utvikling)

        ### Box som grupper Layout for Testing-knappene ###
        testing_box = QGroupBox('Testing')  # Testing (testing av utivklingssett og testsett)
        testing_box.setLayout(testing_layout)
        testing_box.setAlignment(Qt.AlignTop)

        ### Overordnet Layout for knappene til høyre ###
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.setSpacing(width * 0.005)  # Mellomrom mellom hver knapp
        button_layout.addWidget(UI_Valgte_Filer.kjorTesting)
        button_layout.addWidget(self.legg_til_fil)
        button_layout.addWidget(self.eksporter)
        button_layout.addWidget(self.tilbake)
        button_layout.addWidget(self.kjorDeteksjon)

        ### Overorndet Box som grupper Layout for knappene til høyre ###
        button_box = QGroupBox("")  # Knapper
        button_box.setLayout(button_layout)
        button_box.setAlignment(Qt.AlignBottom)

        ### Overordnet Layout for Tabell ###
        table_layout = QVBoxLayout()
        table_layout.addWidget(tabell_box)

        ### Overorndet Layout for alle knappene ###
        action_layout = QHBoxLayout()
        action_layout.addWidget(modus_box)  # Ulike modusene (Hurtig og Sakte)
        action_layout.addWidget(dev_box)  # Utviklingsmodus aktiv eller ikke
        action_layout.addWidget(testing_box)  # Testing (testsett eller utviklingssett)
        action_layout.addWidget(button_box)  # Ulike knapper for Legge til filer, Tilbake og Kjør Deteksjon

        ### Overodnet Layout for Logo og Brukerguiden ###
        head_layout = QHBoxLayout()
        head_layout.addWidget(hjelp_box)
        head_layout.addWidget(logo_box)

        ### FOR-Loop for føring av filer inn i tabell ###
        for i in range(len(MainWindow.arr)):

            size = os.path.getsize(MainWindow.arr[i])  # Henter størrelsen på hver fil i KB

            sizeMB = (size / 1000000)  # Omgjøring til MB
            sizeMB = np.round(sizeMB, 2)

            clip = VideoFileClip(MainWindow.arr[i])

            clip_min = (clip.duration / 60)  # Tillater 10 tegn totalt f.eks 11.1234567

            rowPosition = self.tabell.rowCount()
            self.tabell.insertRow(rowPosition)
            self.tabell.setItem(rowPosition, 0, QTableWidgetItem(str(MainWindow.arr[i])))
            self.tabell.setItem(rowPosition, 1, QTableWidgetItem("%s MB" % sizeMB))

            if float(clip_min) < 1:
                clip = str(clip.duration)
                self.tabell.setItem(rowPosition, 2, QTableWidgetItem("%s sekunder" % clip))

            else:
                self.tabell.setItem(rowPosition, 2, QTableWidgetItem("%s minutter" % clip_min))

            self.tabell.resizeRowsToContents()  # Resize for at hele filnavnet skal komme med

        if UI_Valgte_Filer.kjorTesting.clicked:
            UI_Valgte_Filer.kjorTesting.clicked.connect(MainWindow.kjor_testing)

        if self.tilbake.clicked:
            self.tilbake.clicked.connect(MainWindow.start_UI_Innlesing)

        if self.hjelp.clicked:
            self.hjelp.clicked.connect(MainWindow.show_help)

        if self.legg_til_fil.clicked:  # Om Legg til fil knappen velges så åpnes filvelgeren på nytt
            self.legg_til_fil.clicked.connect(MainWindow.velg_fil)

        if self.kjorDeteksjon.clicked:  # Om Kjør Deteksjon knappen velges så skal Deteksjon.py starte
            self.kjorDeteksjon.clicked.connect(MainWindow.kjor_deteksjon)

        if self.eksporter.clicked:  # Knapp for valg av resultatmappe
            self.eksporter.clicked.connect(MainWindow.eksporter)

        ### Grupperende layout som inkluderer de øvrige layoutene ###
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignLeading)
        main_layout.addLayout(head_layout)
        main_layout.addLayout(table_layout)
        main_layout.addLayout(action_layout)

        ### Setter CentralWidget sitt Layout til main_layout ###
        self.centralwidget.setLayout(main_layout)

        ### Endrer CentralWidget til MainWindow til å benytte UI_Valgte_Filer sin CentralWidget ###
        MainWindow.setCentralWidget(self.centralwidget)


### Vindu 3 - Deteksjon Ferdig ###
class UI_Deteksjon_Ferdig(object):
    def setupUI(self, MainWindow):

        # Oppløsning til skjermen, benyttes for å få korrekt ratio for layout
        screen_shape = QDesktopWidget().screenGeometry()  # Finner størrelse på Window
        width = screen_shape.width()
        height = screen_shape.height()

        self.centralwidget = QWidget(MainWindow)

        self.daf_kort = QLabel('DAF')  # Label som skal være DAF logo/tekst
        self.daf_kort.setStyleSheet('font-size: 25pt; font-family: Open Sans; border: 0px solid;')

        self.daf_lang = QLabel('Deteksjon av Fisk i Video')  # Label som skal være DAF logo/tekst
        self.daf_lang.setStyleSheet('font-size: 18pt; font-family: Open Sans; border: 0px solid;')

        self.hjelp = QPushButton('')  # Hjelp knapp for å vise Brukerguide
        self.hjelp.setIconSize(QSize(width * 0.1, height * 0.1))
        self.hjelp.setStyleSheet('QPushButton{border: 0px solid;}')
        self.hjelp.setIcon(QIcon("Vedlegg/Help.png"))

        self.tabell = QTableWidget()
        self.tabell.setRowCount(0)
        self.tabell.setColumnCount(3)
        self.tabell.setColumnWidth(0, width * 0.45)
        self.tabell.setHorizontalHeaderLabels(["Filnavn", "Filstørrelse", "Lengde"])

        self.ny_innlesing = QPushButton('Ny Innlesing')
        self.ny_innlesing.setStyleSheet('font-size: 18pt; font-family: Open Sans;')

        ### LAYOUT - UI_Deteksjon_Ferdig ###

        ### Layout for Logo ###
        logo_layout = QVBoxLayout()
        logo_layout.addWidget(self.daf_kort, alignment=Qt.AlignRight)
        logo_layout.addWidget(self.daf_lang)
        logo_layout.setAlignment(Qt.AlignRight)

        ### Box som grupper Layout til Logo ###
        logo_box = QGroupBox("")  # Logo + Overskrift
        logo_box.setLayout(logo_layout)
        logo_box.setAlignment(Qt.AlignRight)

        ### Layout for Brukerguiden ###
        hjelp_layout = QVBoxLayout()
        hjelp_layout.addWidget(self.hjelp, alignment=Qt.AlignHCenter)

        ### Box som grupper Layout til Brukerguiden ###
        hjelp_box = QGroupBox("")  # Hjelp knapp
        hjelp_box.setLayout(hjelp_layout)
        hjelp_box.setMaximumWidth(width * 0.125)
        hjelp_box.setAlignment(Qt.AlignLeft)

        ### Layout for Tabellen ###
        tabell_layout = QVBoxLayout()
        tabell_layout.addWidget(self.tabell)

        ### Box som grupper Layout til tabellen ###
        tabell_box = QGroupBox("Filer")  # Tabell med filer
        tabell_box.setLayout(tabell_layout)
        tabell_box.setAlignment(Qt.AlignLeft)

        ### Overordnet Layout for knappene ###
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.ny_innlesing)

        ### Overorndet Box som grupper Layout for knappene ###
        button_box = QGroupBox("")  # Knapper
        button_box.setLayout(button_layout)
        button_box.setAlignment(Qt.AlignBottom)

        ### Overordnet Layout for Tabell ###
        table_layout = QVBoxLayout()
        table_layout.addWidget(tabell_box)

        ### Overorndet Layout for alle knappene ###
        action_layout = QHBoxLayout()
        action_layout.addWidget(button_box)

        ### Overodnet Layout for Logo og Brukerguiden ###
        head_layout = QHBoxLayout()
        head_layout.addWidget(hjelp_box)
        head_layout.addWidget(logo_box)

        ### FOR-Loop for føring av filer inn i tabell ###
        for i in range(len(MainWindow.arr)):

            size = os.path.getsize(MainWindow.arr[i]) # Henter størrelsen på hver fil i KB

            sizeMB = (size / 1000000)  # Omgjøring til MB
            sizeMB = np.round(sizeMB, 2)

            clip = VideoFileClip(MainWindow.arr[i])

            clip_min = (clip.duration / 60)  # Tillater 10 tegn totalt f.eks 11.1234567

            rowPosition = self.tabell.rowCount()
            self.tabell.insertRow(rowPosition)
            self.tabell.setItem(rowPosition, 0, QTableWidgetItem(str(MainWindow.arr[i])))
            self.tabell.setItem(rowPosition, 1, QTableWidgetItem("%s MB" % sizeMB))

            if float(clip_min) < 1:
                clip = str(clip.duration)
                self.tabell.setItem(rowPosition, 2, QTableWidgetItem("%s sekunder" % clip))

            else:
                self.tabell.setItem(rowPosition, 2, QTableWidgetItem("%s minutter" % clip_min))

            self.tabell.resizeRowsToContents()  # Resize for at hele filnavnet skal komme med

        if self.hjelp.clicked:
            self.hjelp.clicked.connect(MainWindow.show_help)

        ### Grupperende layout som inkluderer de øvrige layoutene ###
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignLeading)
        main_layout.addLayout(head_layout)
        main_layout.addLayout(table_layout)
        main_layout.addLayout(action_layout)

        ### Setter CentralWidget sitt Layout til main_layout ###
        self.centralwidget.setLayout(main_layout)

        ### Endrer CentralWidget til MainWindow til å benytte UI_Deteksjons_Ferdig sin CentralWidget ###
        MainWindow.setCentralWidget(self.centralwidget)


class MainWindow(QMainWindow):

    ### GLOBALE VERDIER ###
    filename = []  # Array for innlesing av filer, blir erstattet av arr arrayet.
    arr = []  # Array for innlegging av korrekt filepath fra filename arrayet.
    size = []  # Int for størrelse på innlest fil
    eksporter_path = ""  # Filstien for eksportering

    modus = ""  # Modus detekesjonen skal kjøre i (Sakte / Hurtig)
    datasett = ""  # Datasett som testingen skal kjøre med (Utvilkingssett / Testsett)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        """
        Funksjon initialiserer funksjonen start_UI_Innlesing med spesifisert vindustørrelse og posisjon på skjermen
         
        """

        self.uiInnlesing = UI_Innlesing()
        self.uiValgte_Filer = UI_Valgte_Filer()
        self.uiDeteksjon_Ferdig = UI_Deteksjon_Ferdig()
        self.start_UI_Innlesing()

        screen_size = QApplication.desktop().screenGeometry()  # Dynamisk valg av størrelse på applikasjon

        width = screen_size.width()
        height = screen_size.height()

        w = np.ceil(width * 0.7)  # Runder Bredden opp om desimaltall
        h = np.ceil(height * 0.7)  # Runder Høyde opp om desimaltall

        x = np.ceil(width * 0.15)  # Runder X-koordinaten opp fra desimaltall
        y = np.ceil(height * 0.2)  # Runder Y-koordinaten opp fra desimaltall

        self.setGeometry(x, y, w, h)  # Setter størrelse på applikasjon til å være bredde og høyde ganger 0.7


    def start_UI_Valgte_Filer(self):
        """
        Funskjon initialiserer UI_Valgte_Filer
        """

        MainWindow.uiValgte_Filer.setupUI(self)
        MainWindow.uiValgte_Filer.kjorDeteksjon.clicked.connect(self.kjor_deteksjon)
        MainWindow.show()

    def start_UI_Deteksjon_Ferdig(self):
        """
        Funskjonm initialiserer UI_Deteksjon_Ferdig
        """
        self.uiDeteksjon_Ferdig.setupUI(self)
        self.uiDeteksjon_Ferdig.ny_innlesing.clicked.connect(self.start_UI_Innlesing)

        ### Deteksjon er fullført, vis melding###
        hovedtekst = "Fullført!"
        informasjonstekst = "Deteksjonen har nå kjørt ferdig"
        self.show_popup(hovedtekst, informasjonstekst)

        self.show()

    def start_UI_Innlesing(self):
        """
        Funksjon definerer tittel på vinduet og initialiserer UI_Innlesing

        """
        self.setWindowTitle("Deteksjon av Fisk i Video")
        self.uiInnlesing.setupUI(self)
        MainWindow.arr = []  # Initialiserer et tomt array for filnavnene
        self.uiInnlesing.innlesing_knapp.clicked.connect(self.velg_fil)
        self.uiInnlesing.hjelp.clicked.connect(self.show_help)
        self.show()

    def velg_fil(self):
        """
        Funksjon for å velge filer som det skal gjøres deteksjon på

        Gjennomfører sjekk for duplikater gjennom 'duplikater(element)'.
        Kontrollere at duplikater ikke inkluderes om bruker filer som allerede er lastet inn.

        :return: Array med filer (MainWindow.arr)
        """

        filter = "All Files (*);;MP4 (*.mp4);;M4V (*.m4v);;MOV (*.mov)"  # Filter for QFileDialog
        MainWindow.filename = QFileDialog.getOpenFileNames(self, "Velg video", "", filter)
        MainWindow.filename = list(MainWindow.filename)
        MainWindow.filename.pop(len(MainWindow.filename) - 1)  # Fjerner siste element som er "MP4 (*.mp4)"

        for file in MainWindow.filename:
            MainWindow.arr += file

        def duplikater(element): # Sjekker for duplikater om noen velger samme fil igjen gjennom "Legg til fil"-knappen
            return list(dict.fromkeys(element))

        MainWindow.arr = duplikater(MainWindow.arr) # Setter nytt array til å være lik arrayet med kun unike elementer

        if np.size(MainWindow.arr) >= 1: # Om det er valgt 1 fil eller mer
            self.uiValgte_Filer.setupUI(self)
            self.show()

    def kjor_deteksjon(self):
        """
        Funksjon for kjøre deteksjon på valgte filer

        If-else sjekk for Modus og Utviklingsmodus som deteksjonen skal kjøres med
        """

        ### Deteksjon: Modus ###
        state_sakte = UI_Valgte_Filer.sakte.isChecked()  # Checked state = True, Not checked state = False
        state_hurtig = UI_Valgte_Filer.hurtig.isChecked()

        ### Sjekker hvilken modus brukeren har valgt ###
        if state_sakte is True and state_hurtig is True:  # Om begge modusene er valgt (skal være fysisk umulig)
            print("Denne meldingen skal aldri vises")
            return

        elif state_sakte is True and state_hurtig is False:
            print("Modus: Sakte")

            MainWindow.modus = "Sakte"  # Modus "Sakte" er valgt

        elif state_sakte is False and state_hurtig is True:
            print("Modus: Hurtig")

            MainWindow.modus = "Hurtig"  # Modus "Hurtig" er valgt

        else:  # Om ingen av modusene er valgt
            print("Vennligst velg en modus")
            hovedtekst = "Modus:"
            informasjonstekst = "Vennligst velg én modus"
            MainWindow.show_popup(self, hovedtekst, informasjonstekst)
            return


        ### Deteksjon: Utviklingsmodus ###
        state_devMode = UI_Valgte_Filer.devMode.checkState()  # Sjekk om Utviklingsmodus er aktivert eller ikke

        if state_devMode == 2:  # 2 = aktiv, 0 = inaktiv
            MainWindow.devMode = True
            print("Utviklingsmodus: Aktivert")

        else:
            MainWindow.devMode = False
            print("Utvilingsmodus: Deaktivert")

        ### Kjør deteksjon med valgte paramertre ###
        Deteksjon.path(MainWindow.filename, MainWindow.modus, MainWindow.devMode, MainWindow.eksporter_path)

        self.start_UI_Deteksjon_Ferdig() #Deteksjon er fullført, endre UI


    def kjor_testing(self):
        """
        Funksjon for å kjøre testing av datasettene (Testsett og Utviklingssett)

        If-else sjekk for Modus, Utviklingsmodus og Datasett som testing skal kjøres med
        """

        ### Deteksjon: Modus ###
        state_sakte = UI_Valgte_Filer.sakte.isChecked()  # Checked state = True, Not checked state = False
        state_hurtig = UI_Valgte_Filer.hurtig.isChecked()

        ### Testing: Datasett ###
        state_testsett = UI_Valgte_Filer.testing_test.isChecked()  # Checked state = 2, Not checked state = 0
        state_utviklingssett = UI_Valgte_Filer.testing_utvikling.isChecked()

        if state_sakte is not False or state_hurtig is not False:
            if state_testsett is True and state_utviklingssett is True:
                print("Denne meldingen skal aldri vises")

                return

            elif state_testsett is False and state_utviklingssett is False:
                #print("Må velge ett av datasettene når testing skal kjøres")
                hovedtekst = "Testing:"
                informasjonstekst = "Må velge ett av datasettene"
                MainWindow.show_popup(self, hovedtekst, informasjonstekst)
                return

            elif state_testsett is True and state_sakte is True:
                MainWindow.datasett = "Testsett"  # Datasettet testsett er valgt
                MainWindow.modus = "Sakte"

            elif state_testsett is True and state_hurtig is True:
                MainWindow.datasett = "Testsett"  # Datasettet utviklingssett er valgt
                MainWindow.modus = "Hurtig"

            elif state_utviklingssett is True and state_sakte is True:
                MainWindow.datasett = "Utviklingssett"  # Datasettet utviklingssett er valgt
                MainWindow.modus = "Sakte"

            elif state_utviklingssett is True and state_hurtig is True:
                MainWindow.datasett = "Utviklingssett"  # Datasettet utviklingssett er valgt
                MainWindow.modus = "Hurtig"


            ### Deteksjon: Utviklingsmodus ###
            state_devMode = UI_Valgte_Filer.devMode.checkState()  # Sjekk om Utviklingsmodus er aktivert eller ikke
            if state_devMode == 2:  # 2 = aktiv, 0 = inaktiv
                MainWindow.devMode = True
                print("Utviklingsmodus: Aktivert")

            else:
                MainWindow.devMode = False
                print("Utvilingsmodus: Deaktivert")

            # Kjør testing med valgt datasett
            Deteksjon.testing(MainWindow.datasett, MainWindow.modus, MainWindow.devMode, MainWindow.eksporter_path)
            self.start_UI_Deteksjon_Ferdig()  # Deteksjon er fullført, endre UI


        else:  # En modus må være valgt
            print("En modus må være valgt")
            hovedtekst = "Feilmedling:"
            informasjonstekst = "Må velge en modus før testing kjøres"
            MainWindow.show_popup(self, hovedtekst, informasjonstekst)

            return

    def show_popup(self, hovedtekst, informasjonstekst):
        """
        Funksjon for å vise meldingsbokser.

        :param hovedtekst: String som funksjonen benytter for å sette tekst i meldingsboksen
        :param informasjonsteskt: String som funksjonen benytter for å sette tekst i meldingsboksen
        :return: Meldingsboks-objekt
        """

        screen_size = QApplication.desktop().screenGeometry()  # Dynamisk valg av størrelse
        width = screen_size.width()
        height = screen_size.height()

        msg = QMessageBox()  # Oppretter objektet
        msg.setWindowTitle("Melding")  # Setter tittel på meldingsboksen
        msg.setStyleSheet("QLabel{font-size:24px;}")  # Størrelse på teksten i boksen
        msg.setText(hovedtekst)
        msg.setInformativeText(informasjonstekst)
        msg.setIcon(QMessageBox.Information)  # Setter ikonet til meldingsboksen til å være et Informasjonstegn

        x = msg.exec_()

    def eksporter(self):
        """
        Funksjon for å definere eksporteringsmappe

        :param self: MainWindow object
        :return: mappe_path: Filstien til valgt mappe
        """
        print(self)
        dialog = QFileDialog()
        mappe_path = dialog.getExistingDirectory(self, 'Velg ønsket mappe')  # Mappe som velges
        MainWindow.eksporter_path = mappe_path  # Setter 'MainWindow.eksporter' til å benytte mappen valgt av brukeren

    def show_help(self):
        """
        Funskjonen endrer funksjonskall i henhold til operativsystem

        :return: Brukerguiden
        """

        path = "Vedlegg/Brukerguide.pdf"

        #Om MacOSX (Darwin), ellers Windows
        if sys.platform == 'darwin':
            os.system('open ' + path) #For MacOSX
        else:
            os.system('start ' + path) #For Windows


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())