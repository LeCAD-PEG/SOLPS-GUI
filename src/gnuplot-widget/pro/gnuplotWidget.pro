# This qmake project file is used for internationalization tools.
# run lupdate to update ts files, linguist to edit the translations
# and lrelease to generate the qm files

SOURCES      = gnuplotWidget.cpp moc_gnuplotWidget.cpp moc_QtGnuplotApplication.cpp moc_QtGnuplotEvent.cpp moc_QtGnuplotScene.cpp moc_QtGnuplotWidget.cpp moc_QtGnuplotWindow.cpp qrc_QtGnuplotResource.cpp QtGnuplotApplication.cpp QtGnuplotEvent.cpp QtGnuplotInstance.cpp QtGnuplotItems.cpp QtGnuplotScene.cpp QtGnuplotWidget.cpp QtGnuplotWindow.cpp moc_QtGnuplotInstance.cpp

HEADERS = gnuplotWidget.h moc_QtGnuplotApplication.h moc_QtGnuplotEvent.h moc_QtGnuplotScene.h moc_QtGnuplotWidget.h moc_QtGnuplotWindow.h qrc_QtGnuplotResource.h QtGnuplotApplication.h QtGnuplotEvent.h QtGnuplotInstance.h QtGnuplotItems.h QtGnuplotScene.h QtGnuplotWidget.h QtGnuplotWindow.h
FORMS        = QtGnuplotSettings.ui
TRANSLATIONS = po/qtgnuplot_fr.ts \
               po/qtgnuplot_ja.ts

TARGET = gnuplotWidget
QT += gui core network printsupport svg
CONFIG = c++11
QMAKE_CFLAGS = -pipe -O2 -Wall -W -D_REENTRANT -fPIC -DQT_NO_DEBUG -DQT_GUI_LIB -DQT_CORE_LIB
QMAKE_CXXFLAGS = -pipe -std=c++11 -Wall -W -D_REENTRANT -fPIC -DQT_NO_DEBUG -DQT_GUI_LIB -DQT_CORE_LIB

INCLUDEPATH = . ../../../staging/qt/5.7.1/include ../../../staging/qt/5.7.1/include/QtGui ../../../staging/qt/5.7.1/include/QtCore ../../../staging/qt/5.7.1/include/QtWidgets ../../../staging/qt/5.7.1/include/QtSvg ../../../staging/qt/5.7.1/mkspecs/linux-g++ ../../../staging/qt/5.7.1/include/QtNetwork
LIBS =  -L/home/simicg/solps-gui/staging/qt/5.7.1/lib -lQt5Core -lGL -lpthread -lQt5Widgets -lQt5Svg -lQt5PrintSupport -lQt5Network -lQt5Gui

QMAKE_LFLAGS = -Wl,-O1 -Wl,-rpath,/home/simicg/solps-gui/staging/qt/5.7.1/lib