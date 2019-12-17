from PyQt5.QtWidgets import (QApplication, QGraphicsScene,
                             QGraphicsSceneMouseEvent, QGraphicsItem,
                             QGraphicsRectItem)
from PyQt5.QtGui import (QKeyEvent, QPolygonF, QPen, QBrush, QColor, QPixmap,
                         QPainterPath, QFont, QImage, QFontMetrics)
from PyQt5.QtCore import (QDataStream, QPoint, QPointF, QRectF, Qt, QRect,
                          QLineF, QSizeF, QSize, qRound, QTime)

from QtGnuplot.QtGnuplotEvent import (QtGnuplotEventReceiver, GEMove, GEVector,
                                      GEClear, GELineWidth, GEPenColor,
                                      GEBackgroundColor, GEPenStyle,
                                      GEDashPattern, GEPointSize,
                                      GETextAlignment, GEFillBox,
                                      GEFilledPolygon, GEBrushStyle, GERuler,
                                      GESetFont, GEPoint, GEPutText,
                                      GEEnhancedFlush, GEEnhancedFinish,
                                      GEImage, GEZoomStart, GEZoomStop,
                                      GELineTo, GESetSceneSize, GEScale,
                                      GEAfterPlot, GEPlotNumber,
                                      GEModPlots, GELayer, GEHypertext,
                                      GETextBox, GEFontMetricRequest, GEDone,
                                      GETextAngle,
                                      QTMODPLOTS_INVERT_VISIBILITIES,
                                      QTMODPLOTS_SET_VISIBLE,
                                      QTMODPLOTS_SET_INVISIBLE,
                                      QTLAYER_BEFORE_ZOOM,
                                      QTLAYER_BEGIN_KEYSAMPLE,
                                      QTLAYER_END_KEYSAMPLE)

from QtGnuplot.QtGnuplotItems import (QtGnuplotPoint, QtGnuplotEnhanced,
                                      QtGnuplotClippedPixmap, QtGnuplotKeybox)

import logging
import platform
import math
from QtGnuplot.QtGnuplotItems import QtGnuplotPoints

from QtGnuplot.mousecmn import (GE_motion, GE_buttonpress, GE_buttonrelease,
                                GE_keypress, GE_buttonpress_old,
                                GE_buttonrelease_old, GE_keypress_old,
                                GE_modifier, GE_plotdone, GE_replot, GE_reset,
                                GE_fontprops, GE_pending, GE_raise,
                                GP_BackSpace, GP_Tab, GP_KP_Enter, GP_Return,
                                GP_Escape, GP_Delete,
                                GP_FIRST_KEY, GP_Linefeed, GP_Clear, GP_Pause,
                                GP_Scroll_Lock, GP_Sys_Req, GP_Insert,
                                GP_Home, GP_Left, GP_Up, GP_Right, GP_Down,
                                GP_PageUp, GP_PageDown, GP_End, GP_Begin,
                                GP_KP_Space, GP_KP_Tab, GP_KP_F1, GP_KP_F2,
                                GP_KP_F3, GP_KP_F4, GP_KP_Insert, GP_KP_End,
                                GP_KP_Down, GP_KP_Page_Down, GP_KP_Left,
                                GP_KP_Begin, GP_KP_Right, GP_KP_Home,
                                GP_KP_Up, GP_KP_Page_Up, GP_KP_Delete,
                                GP_KP_Equal, GP_KP_Multiply,
                                GP_KP_Add, GP_KP_Separator, GP_KP_Subtract,
                                GP_KP_Decimal, GP_KP_Divide, GP_KP_0, GP_KP_1,
                                GP_KP_2, GP_KP_3, GP_KP_4, GP_KP_5,
                                GP_KP_6, GP_KP_7, GP_KP_8, GP_KP_9, GP_F1,
                                GP_F2, GP_F3, GP_F4, GP_F5, GP_F6, GP_F7,
                                GP_F8, GP_F9, GP_F10, GP_F11, GP_F12,
                                GP_Cancel, GP_Button1, GP_LAST_KEY)


gnuplot_key_bind = {
    Qt.Key_Space: GP_KP_Space,
    Qt.Key_Tab: GP_KP_Tab,
    Qt.Key_Enter: GP_KP_Enter,
    Qt.Key_F1: GP_KP_F1,
    Qt.Key_F2: GP_KP_F2,
    Qt.Key_F3: GP_KP_F3,
    Qt.Key_F4: GP_KP_F4,
    Qt.Key_Insert: GP_KP_Insert,
    Qt.Key_End: GP_KP_End,
    Qt.Key_Home: GP_KP_Home,
    Qt.Key_PageDown: GP_KP_Page_Down,
    Qt.Key_PageUp: GP_KP_Page_Up,
    Qt.Key_Delete: GP_KP_Delete,
    Qt.Key_Equal: GP_KP_Equal,
    Qt.Key_Asterisk: GP_KP_Multiply,
    Qt.Key_Plus: GP_KP_Add,
    Qt.Key_Comma: GP_KP_Separator,
    Qt.Key_Minus: GP_KP_Subtract,
    Qt.Key_Period: GP_KP_Decimal,
    Qt.Key_Slash: GP_KP_Divide,
    Qt.Key_0: GP_KP_0,
    Qt.Key_1: GP_KP_1,
    Qt.Key_2: GP_KP_2,
    Qt.Key_3: GP_KP_3,
    Qt.Key_4: GP_KP_4,
    Qt.Key_5: GP_KP_5,
    Qt.Key_6: GP_KP_6,
    Qt.Key_7: GP_KP_7,
    Qt.Key_8: GP_KP_8,
    Qt.Key_9: GP_KP_9,
    Qt.Key_Backspace: GP_BackSpace,
    Qt.Key_Tab: GP_Tab,
    Qt.Key_Return: GP_Return,
    Qt.Key_Escape: GP_Escape,
    Qt.Key_Delete: GP_Delete,
    Qt.Key_Pause: GP_Pause,
    Qt.Key_ScrollLock: GP_Scroll_Lock,
    Qt.Key_Insert: GP_Insert,
    Qt.Key_Home: GP_Home,
    Qt.Key_Left: GP_KP_Left,
    Qt.Key_Up: GP_KP_Up,
    Qt.Key_Right: GP_KP_Right,
    Qt.Key_Down: GP_KP_Down,
    Qt.Key_PageUp: GP_PageUp,
    Qt.Key_PageDown: GP_PageDown,
    Qt.Key_End: GP_End,
    Qt.Key_Enter: GP_KP_Enter,
    Qt.Key_F1: GP_F1,
    Qt.Key_F2: GP_F2,
    Qt.Key_F3: GP_F3,
    Qt.Key_F4: GP_F4,
    Qt.Key_F5: GP_F5,
    Qt.Key_F6: GP_F6,
    Qt.Key_F7: GP_F7,
    Qt.Key_F8: GP_F8,
    Qt.Key_F9: GP_F9,
    Qt.Key_F10: GP_F10,
    Qt.Key_F11: GP_F11,
    Qt.Key_F12: GP_F12,
}


if platform.system() == 'Darwin':
    # MAC
    gnuplot_key_bind[Qt.Key_Down] = GP_Down
    gnuplot_key_bind[Qt.Key_Left] = GP_Left
    gnuplot_key_bind[Qt.Key_Right] = GP_Right
    gnuplot_key_bind[Qt.Key_Up] = GP_Up


QtGnuplotBrushes = [Qt.NoBrush, Qt.DiagCrossPattern, Qt.Dense3Pattern,
                    Qt.SolidPattern, Qt.FDiagPattern, Qt.BDiagPattern,
                    Qt.Dense4Pattern, Qt.Dense5Pattern]


FS_EMPTY, FS_SOLID, FS_PATTERN, FS_DEFAULT, FS_TRANPARENT_SOLID, \
    FS_TRANSPARENT_PATTERN = range(6)


class QtGnuplotScene(QGraphicsScene, QtGnuplotEventReceiver):

    def __init__(self, parent):
        QGraphicsScene.__init__(self, parent)
        self.m_widget = parent
        self.m_eventHandler = parent.m_eventHandler

        self.m_currentPolygon = QPolygonF()
        self.m_plot_group = []
        self.m_textAlignment = Qt.AlignLeft
        self.m_currentPen = QPen()
        self.m_currentBrush = QBrush()
        self.m_font = QFont()
        self.m_currentPosition = None
        self.m_zoomBoxCorner = QPoint()
        self.m_currentPointSize = 1.0
        self.m_textAngle = 0.0
        self.m_currentBoxRotation = None
        self.m_currentBoxOrigin = None
        self.m_textOffset = QPoint(10, 10)
        self.m_currentZ = 1.0
        self.m_watches = [QTime() for i in range(4)]
        self.m_currentPlotNumber = 0
        self.m_inKeySample = False
        self.m_preserveVisibility = False
        self.m_inTextBox = False
        self.m_currentFillStyle = None
        self.m_currentTextBox = None
        self.m_textMargin = None
        self.m_currentGroup = []
        self.m_currentPointsItem = QtGnuplotPoints()

        self.m_lastMousePos = QPoint()
        self.m_lastModifierMask = 0

        self.m_horizontalRuler = None
        self.m_verticalRuler = None
        self.m_lineTo = None
        self.m_zoomRect = None
        self.m_zoomStartText = None
        self.m_zoomStopText = None
        self.m_enhanced = 0
        self.m_key_boxes = []
        self.m_currentHypertext = ""
        self.m_hypertextList = []
        self.m_hyperImage = None
        self.m_axisValid = [False for i in range(5)]
        self.m_axisMin = [0.0 for i in range(4)]
        self.m_axisLower = [0.0 for i in range(4)]
        self.m_axisScale = [0.0 for i in range(4)]
        self.m_axisLog = [0.0 for i in range(4)]

        self.resetItems()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if not self.m_widget.isActive():
            if self.m_axisValid[4]:
                # 3D plot
                pass
            else:
                self.m_lineTo.hide()
                s = ''  # Status
                if self.m_axisValid[0]:
                    s += f" x = {self.sceneToGraph(0, event.scenePos().x())}"
                if self.m_axisValid[1]:
                    s += f" y = {self.sceneToGraph(1, event.scenePos().y())}"
                if self.m_axisValid[2]:
                    s += f" x2 = {self.sceneToGraph(2, event.scenePos().x())}"
                if self.m_axisValid[3]:
                    s += f" y2 = {self.sceneToGraph(3, event.scenePos().y())}"
                self.m_widget.setStatusText(s)

            QGraphicsScene.mouseMoveEvent(self, event)
            return

        self.m_lastMousePos = event.scenePos()
        self.updateModifiers()

        if self.m_lineTo.isVisible():
            line = self.m_lineTo.line()
            line.setP2(event.scenePos())
            self.m_lineTo.setLine(line)

        # The first item in m_hypertextList is always a background rectangle
        # for the text
        i = len(self.m_hypertextList)
        hit = False
        while i > 1:
            i -= 1
            if not hit and (self.m_hypertextList[i].pos() - self.m_textOffset -
                            self.m_lastMousePos).manhattanLength() <= 5:
                hit = True
                self.m_hypertextList[i].setVisible(True)
                self.m_hypertextList[0].setRect(self.m_hypertextList[i].boundingRect())
                self.m_hypertextList[0].setPos(self.m_hypertextList[i].pos())
                self.m_hypertextList[0].setZValue(self.m_hypertextList[i].zValue()-1)

                # Special hypertext "image{(xsize,ysize)}:filename"
                current_text = self.m_hypertextList[i].toPlainText()
                if current_text.startswith("image"):
                    sep = current_text.index(":")
                    imagename = current_text[sep+1:].rstrip()
                    self.m_hyperImage.setPixmap(QPixmap(imagename))
                    self.m_hyperImage.setVisible(True)
                    break
            else:
                self.m_hypertextList[i].setVisible(False)
                self.m_hyperImage.setVisible(False)
        self.m_hypertextList[0].setVisible(hit)
        self.m_eventHandler.postTermEvent(GE_motion, int(event.scenePos().x()),
            int(event.scenePos().y()), 0, 0, self.m_widget)
        QGraphicsScene.mouseMoveEvent(self, event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.m_lastMousePos = event.scenePos()
        self.updateModifiers()

        button = 0

        if event.button() == Qt.LeftButton:
            button = 1
        elif event.button() == Qt.MidButton:
            button = 2
        elif event.button() == Qt.RightButton:
            button = 3

        self.m_eventHandler.postTermEvent(GE_buttonpress,
            int(event.scenePos().x()), int(event.scenePos().y()),
                button, 0, self.m_widget)

        QGraphicsScene.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.m_lastMousePos = event.scenePos()
        self.updateModifiers()

        button = 0
        if event.button() == Qt.LeftButton:
            button = 1
        elif event.button() == Qt.MidButton:
            button = 2
        elif event.button() == Qt.RightButton:
            button = 3

        time = 301
        if self.m_watches[button].isValid():
            time = self.m_watches[button].elapsed()
        self.m_eventHandler.postTermEvent(GE_buttonrelease,
            int(event.scenePos().x()), int(event.scenePos().y()),
                button, time, self.m_widget)
        self.m_watches[button].start()

        if button == 1:
            n = len(self.m_key_boxes)
            for i in range(n):
                state = self.m_key_boxes[i].contains(self.m_lastMousePos)
                if state:
                    if self.m_plot_group[i].isVisible():
                        self.m_plot_group[i].setVisible(False)
                        self.m_key_boxes[i].setHidden(True)
                    else:
                        self.m_plot_group[i].setVisible(True)
                        self.m_key_boxes[i].setHidden(False)
                    self.m_preserveVisibility = True
                    break
        QGraphicsScene.mouseReleaseEvent(self, event)

    def wheelEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.updateModifiers()
        if event.orientation() == Qt.Horizontal:
            delta = 6 if event.delta() > 6 else 7
            self.m_eventHandler.postTermEvent(GE_buttonpress,
                int(event.scenePos().x()), int(event.scenePos().y()),
                    delta, 0, self.m_widget)
        else:
            delta = 4 if event.delta() > 6 else 5
            self.m_eventHandler.postTermEvent(GE_buttonpress,
                int(event.scenePos().x()), int(event.scenePos().y()),
                    delta, 0, self.m_widget)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.updateModifiers()
        key = -1
        live = -1
        eventKey = event.key()
        if event.modifiers() and Qt.KeypadModifier:
            if eventKey in gnuplot_key_bind:
                key = gnuplot_key_bind[eventKey]
        elif eventKey <= 0xff and event.text() != '':
            key = ord(event.text()[0])
        else:
            if eventKey in gnuplot_key_bind:
                key = gnuplot_key_bind[eventKey]

        if key == GP_Tab:
            key = 0

        if key >= 0:
            live = self.m_eventHandler.postTermEvent(GE_keypress,
                int(self.m_lastMousePos.x()), int(self.m_lastMousePos.y()),
                key, 0, self.m_widget)
        else:
            live = True

        if not live:
            if key == 'i':
                i = len(self.m_key_boxes)
                if i > len(self.m_plot_group):
                    i = len(self.m_plot_group)

                while i > 0:
                    i -= 1
                    isVisible = not self.m_plot_group[i].isVisible()
                    self.m_plot_group[i].setVisible(isVisible)
                    self.m_key_boxes[i].setHidden(not isVisible)

        QGraphicsScene.keyPressEvent(self, event)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if Qt.Key_Tab == event.key():
            self.m_eventHandler.postTermEvent(GE_keypress,
                int(self.m_lastMousePos.x()), int(self.m_lastMousePos.y()),
                GP_Tab, 0, self.m_widget)
        QGraphicsScene.keyReleaseEvent(self, event)

    def processEvent(self, type: int, dataStream: QDataStream) -> None:
        # logging.debug(f"GnuplotGraphicsScene processEvent {type}")
        if type != GEMove and type != GEVector and not self.m_currentPolygon.isEmpty():
            logging.debug("Flushing current polygon")
            point = self.m_currentPolygon.last()
            self.flushCurrentPolygon()
            self.m_currentPolygon << point
        if type == GEClear:
            logging.debug("GnuplotGraphicScene::GEClear")
            self.resetItems()
        elif type == GELineWidth:
            logging.debug("GnuplotGraphicScene::GELineWidth")
            width = dataStream.readDouble()
            logging.debug(f"Linewidth: {width}")
            self.m_currentPen.setWidth(width)
        elif type == GEMove:
            logging.debug("GnuplotGraphicScene::GEMove")
            point = QPointF(dataStream.readDouble(), dataStream.readDouble())

            if not self.m_currentPolygon.isEmpty() and self.m_currentPolygon.last() != point:
                self.flushCurrentPolygon()
                # self.m_currentPolygon.clear()
            self.m_currentPolygon << point
        elif type == GEVector:
            logging.debug("GnuplotGraphicScene::GEVector")
            # point = QPointF(dataStream.readDouble(), dataStream.readDouble())
            point = QPointF()
            dataStream >> point
            self.m_currentPolygon << point
            if self.m_inKeySample:
                self.flushCurrentPointsItem()
                self.update_key_box(QRectF(point, QSizeF(0, 1)))
        elif type == GEPenColor:
            logging.debug("GnuplotGraphicScene::GEPenColor")
            color = QColor()
            dataStream >> color
            self.m_currentPen.setColor(color)
        elif type == GEBackgroundColor:
            logging.debug("GnuplotGraphicScene::GEBackgroundColor")
            self.m_currentPen.setColor(self.m_widget.backgroundColor())
        elif type == GEPenStyle:
            logging.debug("GnuplotGraphicScene::GEPenStyle")
            style = dataStream.readInt()
            self.m_currentPen.setStyle(Qt.PenStyle(style))
            if self.m_widget.m_rounded:
                self.m_currentPen.setJoinStyle(Qt.RoundJoin)
                self.m_currentPen.setCapStyle(Qt.RoundCap)
            else:
                self.m_currentPen.setJoinStyle(Qt.MiterJoin)
                self.m_currentPen.setCapStyle(Qt.FlatCap)
        elif type == GEDashPattern:
            logging.debug("GnuplotGraphicScene::GEDashPattern")
            n = dataStream.readUInt32()
            # dataStream.readQVariantList()
            dashPattern = [dataStream.readInt() for i in range(n)]
            self.m_currentPen.setDashPattern(dashPattern)
        elif type == GEPointSize:
            logging.debug("GnuplotGraphicScene::GEPointSize")
            self.m_currentPointSize = dataStream.readDouble()
        elif type == GETextAngle:
            logging.debug("GnuplotGraphicScene::GETextAngle")
            self.m_textAngle = dataStream.readDouble()
        elif type == GETextAlignment:
            logging.debug("GnuplotGraphicScene::GETextAlignment")
            alignment = dataStream.readInt()
            self.m_textAlignment = Qt.Alignment(alignment)
        elif type == GEFillBox:
            logging.debug("GnuplotGraphicScene::GEFillBox")
            self.flushCurrentPointsItem()
            rect = QRect()
            dataStream >> rect
            rectItem = QGraphicsRectItem()
            pen = QPen(Qt.NoPen)
            rectItem = self.addRect(QRectF(rect), pen, self.m_currentBrush)
            rectItem.setZValue(self.m_currentZ)
            self.m_currentZ += 1
            if self.m_inKeySample:
                self.update_key_box(rect)
            else:
                self.m_currentGroup.append(rectItem)
        elif type == GEFilledPolygon:
            logging.debug("GnuplotGraphicScene::GEFilledPolygon")
            polygon = QPolygonF()
            dataStream >> polygon

            if not self.m_inKeySample:
                # Distinguish between opaque and transparent pattern fill
                if self.m_currentFillStyle == FS_PATTERN:
                    self.m_currentPointsItem.addFilledPolygon(
                        self.clipPolygon(polygon, False),
                        QBrush(self.m_widget.backgroundColor()))
                self.m_currentPointsItem.addFilledPolygon(
                    self.clipPolygon(polygon, False), self.m_currentBrush)
            else:
                self.flushCurrentPointsItem()
                pen = QPen(Qt.NoPen)
                if self.m_currentBrush.style() == Qt.SolidPattern:
                    pen.setColor(self.m_currentBrush.color())
                path = self.addPolygon(self.clipPolygon(polygon, False),
                                       pen, self.m_currentBrush)
                path.setZValue(self.m_currentZ)
                self.m_currentZ += 1
        elif type == GEBrushStyle:
            logging.debug("GnuplotGraphicScene::GEBrushStyle")
            style = dataStream.readInt()
            self.setBrushStyle(style)
        elif type == GERuler:
            logging.debug("GnuplotGraphicScene::GERuler")
            point = QPoint()
            dataStream >> point
            self.updateRuler(point)
        elif type == GESetFont:
            logging.debug("GnuplotGraphicScene::GESetFont")
            fontName = dataStream.readQString()
            size = dataStream.readInt()
            self.m_font.setFamily(fontName)
            self.m_font.setPointSize(size)
            self.m_font.setStyleStrategy(QFont.ForceOutline)
        elif type == GEPoint:
            logging.debug("GnuplotGraphicScene::GEPoint")
            point = QPointF()
            dataStream >> point
            style = dataStream.readInt()

            self.m_currentPen.setStyle(Qt.SolidLine)

            if not self.m_inKeySample:
                self.m_currentPointsItem.addPoint(self.clipPoint(point),
                    style, self.m_currentPointSize, self.m_currentPen)
            else:
                self.flushCurrentPointsItem()
                pointItem = QtGnuplotPoint(style, self.m_currentPointSize,
                    self.m_currentPen)
                pointItem.setPos(self.clipPoint(point))
                pointItem.setZValue(self.m_currentZ)
                self.m_currentZ += 1
                self.addItem(pointItem)
                self.update_key_box(QRectF(point, QSizeF(2, 2)))

            # Create a hypertext label that will become visible on mouseover.
            # The Z offset is a kludge to force the label into the foreground.
            if self.m_currentHypertext:
                textItem = self.addText(self.m_currentHypertext,
                                        self.m_font)
                textItem.setPos(point + self.m_textOffset)
                textItem.setZValue(self.m_currentZ + 10000)
                textItem.setVisible(False)
                self.m_hypertextList.append(textItem)
                self.m_currentHypertext = ""
        elif type == GEPutText:
            logging.debug("GnuplotGraphicScene::GEPutText")
            self.flushCurrentPointsItem()
            point = QPoint()
            dataStream >> point
            text = dataStream.readQString()
            logging.debug(f"GEPutTExt: {text}")
            textItem = self.addText(text, self.m_font)
            textItem.setDefaultTextColor(self.m_currentPen.color())
            self.positionText(textItem, point + self.m_textOffset)

            rect = textItem.boundingRect()
            if self.m_textAlignment & Qt.AlignCenter:
                rect.moveCenter(point)
                rect.moveBottom(point.y())
            elif self.m_textAlignment & Qt.AlignRight:
                rect.moveBottomRight(point)
            else:
                rect.moveBottomLeft(point)

            rect.adjust(12, rect.height() * 0.67, 0, rect.height() * 0.25)
            if self.m_inKeySample:
                self.update_key_box(rect)
            else:
                self.m_currentGroup.append(textItem)

            if self.m_inTextBox:
                self.m_currentTextBox = self.m_currentTextBox.united(rect)
                self.m_currentBoxRotation = self.m_textAngle
                self.m_currentBoxOrigin = point
        elif type == GEEnhancedFlush:
            logging.debug("GnuplotGraphicScene::GEEnhancedFlush")
            self.flushCurrentPointsItem()
            fontName = dataStream.readQString()
            fontSize = dataStream.readDouble()
            fontStyle = dataStream.readInt()
            fontWeight = dataStream.readInt()
            base = dataStream.readDouble()
            widthFlag = dataStream.readBool()
            showFlag = dataStream.readBool()
            overprint = dataStream.readInt()
            text = dataStream.readQString()

            if isinstance(fontName, bytes):
                fontName = fontName.decode()
            if isinstance(text, bytes):
                text = text.decode('utf-8')

            text.encode()

            if self.m_enhanced == 0:
                self.m_enhanced = QtGnuplotEnhanced()

            self.m_enhanced.addText(fontName, fontSize, QFont.Style(fontStyle),
                                    QFont.Weight(fontWeight), base, widthFlag,
                                    showFlag, overprint, text,
                                    self.m_currentPen.color())
        elif type == GEEnhancedFinish:
            logging.debug("GnuplotGraphicScene::GEEnhancedFinish")
            self.flushCurrentPointsItem()
            point = QPoint()
            dataStream >> point
            self.positionText(self.m_enhanced, point)
            self.m_enhanced.setZValue(self.m_currentZ)
            self.m_currentZ += 1
            self.addItem(self.m_enhanced)

            rect = self.m_enhanced.boundingRect()
            if self.m_textAlignment & Qt.AlignCenter:
                rect.moveCenter(point)
                rect.moveBottom(point.y())
            elif self.m_textAlignment & Qt.AlignRight:
                rect.moveBottomRight(point)
            else:
                rect.moveBottomLeft(point)
            rect.adjust(-self.m_currentPen.width() * 2, rect.height() / 2,
                         self.m_currentPen.width() * 2, rect.height() / 2)
            if self.m_inKeySample:
                self.update_key_box(rect)
            else:
                self.m_currentGroup.append(self.m_enhanced)
            if self.m_inTextBox:
                self.m_currentTextBox |= rect
                self.m_currentBoxRotation = self.m_textAngle
                self.m_currentBoxOrigin = point

            self.m_enhanced = 0

        elif type == GEImage:
            logging.debug("GnuplotGraphicScene::GEImage")
            self.flushCurrentPointsItem()
            p0 = QPointF()
            p1 = QPointF()
            p2 = QPointF()
            p3 = QPointF()
            dataStream >> p0
            dataStream >> p1
            dataStream >> p2
            dataStream >> p3
            image = QImage()
            dataStream >> image

            size = QSize(p1.x() - p0.x(), p1.y() - p0.y())
            clipRect = self.clipRect(QRectF(p2 - p0, p3 - p0))
            pixmap = QPixmap.fromImage(image).scaled(size,
                                                     Qt.IgnoreAspectRatio,
                                                     Qt.FastTransformation)
            item = QtGnuplotClippedPixmap(clipRect, pixmap)
            self.addItem(item)
            item.setZValue(self.m_currentZ)
            self.m_currentZ += 1
            item.setPos(p0)
            self.m_currentGroup.append(item)
        elif type == GEZoomStart:
            logging.debug("GnuplotGraphicScene::GEZoomStart")
            text = dataStream.readQString()
            if isinstance(text, bytes):
                text = text.decode()
            self.m_zoomBoxCorner = self.m_lastMousePos
            self.m_zoomRect.setRect(QRectF())
            self.m_zoomRect.setVisible(True)
            self.m_zoomStartText.setVisible(True)
            self.m_zoomStartText.setPlainText(text)
            size = self.m_zoomStartText.boundingRect().size()
            self.m_zoomStartText.setPos(self.m_zoomBoxCorner -
                QPoint(size.width(), size.height()))
        elif type == GEZoomStop:
            logging.debug("GnuplotGraphicScene::GEZoomStop")
            text = dataStream.readQString()
            if text == "":
                self.m_zoomRect.setVisible(False)
                self.m_zoomStartText.setVisible(False)
                self.m_zoomStopText.setVisible(False)
            else:
                self.m_zoomStopText.setVisible(True)
                if isinstance(text, bytes):
                    text = text.decode()
                self.m_zoomStopText.setPlainText(text)
                self.m_zoomStopText.setPos(self.m_lastMousePos)
                self.m_zoomRect.setRect(
                    QRectF(self.m_zoomBoxCorner + QPointF(0.5, 0.5),
                           self.m_lastMousePos + QPointF(0.5, 0.5)).normalized())
        elif type == GELineTo:
            logging.debug("GnuplotGraphicScene::GELineTo")
            visible = dataStream.readBool()
            self.m_lineTo.setVisible(visible)
            if visible:
                line = self.m_lineTo.line()
                line.setP2(self.m_lastMousePos)
                self.m_lineTo.setLine(line)
        elif type == GESetSceneSize:
            logging.debug("GnuplotGraphicScene::GESetSceneSize")
            width = dataStream.readInt()
            height = dataStream.readInt()
            # self.setSceneRect(QRectF(QPointF(0, 0), QPointF(width, height)))
            self.setSceneRect(0, 0, width, height)
        elif type == GEScale:
            logging.debug("GnuplotGraphicScene::GEScale")
            for i in range(4):
                self.m_axisValid[i] = dataStream.readBool()
                self.m_axisMin[i] = dataStream.readDouble()
                self.m_axisLower[i] = dataStream.readDouble()
                self.m_axisScale[i] = dataStream.readDouble()
                self.m_axisLog[i] = dataStream.readDouble()
            self.m_axisValid[4] = dataStream.readBool()
        elif type == GEAfterPlot:
            logging.debug("GnuplotGraphicScene::GEAfterPlot")
            self.flushCurrentPointsItem()
            if self.m_currentPlotNumber > len(self.m_plot_group):
                newgroup = self.createItemGroup(self.m_currentGroup)
                newgroup.setZValue(self.m_currentZ)
                self.m_currentZ += 1
                if 0 < self.m_currentPlotNumber and self.m_currentPlotNumber <= len(self.m_key_boxes):
                    newgroup.setVisible(not self.m_key_boxes[self.m_currentPlotNumber - 1].isHidden())
                self.m_plot_group.insert(self.m_currentPlotNumber, newgroup)

            if self.m_currentPlotNumber > len(self.m_key_boxes):
                empty = QtGnuplotKeybox(QRectF(QPointF(0, 0), QPointF(0, 0)))
                self.m_key_boxes.insert(self.m_currentPlotNumber, empty)
                self.m_key_boxes[self.m_currentPlotNumber - 1].resetStatus()

            self.m_currentPlotNumber = 0

        elif type == GEPlotNumber:
            logging.debug("GnuplotGraphicScene::GEPlotNumber")
            self.flushCurrentPointsItem()
            newPlotNumber = dataStream.readInt()
            if newPlotNumber > len(self.m_plot_group):
                self.m_currentGroup = []
            self.m_currentPlotNumber = newPlotNumber

        elif type == GEModPlots:
            logging.debug("GnuplotGraphicScene::GEModPlots")
            i = len(self.m_key_boxes)
            ops_i = dataStream.readUInt32()
            plotno = dataStream.readInt()
            if i > len(self.m_plot_group):
                i = len(self.m_plot_group)

            while i > 0:
                i -= 1

                if plotno >= 0 and i != plotno:
                    continue

                isVisible = self.m_plot_group[i].isVisible()

                if ops_i == QTMODPLOTS_INVERT_VISIBILITIES:
                    isVisible = not isVisible
                elif ops_i == QTMODPLOTS_SET_VISIBLE:
                    isVisible = True
                elif ops_i == QTMODPLOTS_SET_INVISIBLE:
                    isVisible = False

                self.m_plot_group[i].setVisible(isVisible)
                self.m_key_boxes[i].setHidden(not isVisible)
        elif type == GELayer:
            logging.debug("GnuplotGraphicScene::GELayer")
            self.flushCurrentPointsItem()
            layer = dataStream.readInt()
            logging.debug(f"GnuplotGraphicScene::GELayer {layer}")

            if layer == QTLAYER_BEFORE_ZOOM:
                self.m_preserveVisibility = True
            if layer == QTLAYER_BEGIN_KEYSAMPLE:
                self.m_inKeySample = True

            if layer == QTLAYER_END_KEYSAMPLE:
                self.m_inKeySample = False
                # FIXME: this catches mislabeled opaque keyboxes in multiplot mode
                if self.m_currentPlotNumber > len(self.m_key_boxes):
                    return

                # Draw an invisible grey rectangle in the key box.
                # It will be set to visible if the plot is toggled off.
                keybox = self.m_key_boxes[self.m_currentPlotNumber - 1]
                self.m_currentBrush.setColor(Qt.lightGray)
                self.m_currentBrush.setStyle(Qt.Dense4Pattern)
                pen = QPen(Qt.NoPen)
                statusBox = self.addRect(keybox, pen, self.m_currentBrush)
                statusBox.setZValue(self.m_currentZ)
                keybox.showStatus(statusBox)

        elif type == GEHypertext:
            logging.debug("GnuplotGraphicScene::GEHypertext")
            self.m_currentHypertext = ''
            self.m_currentHypertext = dataStream.readQString()

        elif type == GETextBox:
            logging.debug("GnuplotGraphicScene::GETextBox")
            self.flushCurrentPointsItem()
            point = QPointF()
            dataStream >> point
            option = dataStream.readInt()

            rectItem = QGraphicsRectItem()
            outline = QRectF()

            TEXTBOX_INIT, TEXTBOX_OUTLINE, TEXTBOX_BACKGROUNDFILL, \
            TEXTBOX_MARGINS, TEXTBOX_FINISH, TEXTBOX_GREY = range(6)

            if option == TEXTBOX_INIT:
                self.m_currentTextBox = QRectF(point, point)
                self.m_inTextBox = True
            elif option == TEXTBOX_OUTLINE:
                outline = self.m_currentTextBox.adjusted(
                    -self.m_textMargin.x(), -self.m_textMargin.y(),
                    self.m_textMargin.x(), self.m_textMargin.y())
                rectItem = self.addRect(outline, self.m_currentPen, Qt.NoBrush)
                rectItem.setZValue(self.m_currentZ)
                self.m_currentZ += 1
                rectItem.setTransformOriginPoint(self.m_currentBoxOrigin)
                rectItem.setRotation(-self.m_currentBoxRotation)
                self.m_currentGroup.append(rectItem)
                self.m_inTextBox = False
            elif option == TEXTBOX_BACKGROUNDFILL:
                self.m_currentBrush.setColor(self.m_currentPen.color())
                self.m_currentBrush.setStyle(Qt.SolidPattern)
                outline = self.m_currentTextBox.adjusted(
                     -self.m_textMargin.x(), -self.m_textMargin.y(),
                      self.m_textMargin.x(), self.m_textMargin.y())
                pen = QPen()
                pen.setStyle(Qt.NoPen)
                rectItem = self.addRect(outline, pen, self.m_currentBrush)
                rectItem.setZValue(self.m_currentZ)
                self.m_currentZ += 1
                rectItem.setTransformOriginPoint(self.m_currentBoxOrigin)
                rectItem.setRotation(-self.m_currentBoxRotation)
                self.m_currentGroup.append(rectItem)
                self.m_inTextBox = False
            elif option == TEXTBOX_MARGINS:
                self.m_textMargin = point
                self.m_textMargin *= QFontMetrics(self.m_font).averageCharWidth()

        elif type == GEFontMetricRequest:
            logging.debug("GnuplotGraphicScene::GEFontMetricRequest")
            metrics = QFontMetrics(self.m_font)
            par1 = metrics.ascent() + metrics.descent()
            par2 = metrics.width("0123456789") // 10
            self.m_eventHandler.postTermEvent(GE_fontprops, 0, 0, par1, par2, self.m_widget)

        elif type == GEDone:
            logging.debug("GnuplotGraphicScene::GEDone")
            self.flushCurrentPointsItem()
            self.m_eventHandler.postTermEvent(GE_plotdone, 0, 0, 0, 0, self.m_widget)

        else:
            self.swallowEvent(type, dataStream)

    def resetItems(self) -> None:
        self.clear()
        self.m_currentPointsItem = QtGnuplotPoints()

        self.m_currentZ = 1.0

        self.m_zoomRect = self.addRect(QRectF(), QPen(QColor(0, 0, 0, 200)),
                                       QBrush(QColor(0, 0, 255, 40)))
        self.m_zoomRect.setVisible(False)
        self.m_zoomRect.setZValue(32767)

        self.m_zoomStartText = self.addText("")
        self.m_zoomStartText.setVisible(False)
        self.m_zoomStartText.setZValue(32767)
        self.m_zoomStopText = self.addText("")
        self.m_zoomStopText.setVisible(False)
        self.m_zoomStopText.setZValue(32767)
        logging.debug(f'\t{self.width()} {self.height()}')
        self.m_horizontalRuler = self.addLine(QLineF(0, 0, self.width(), 0),
                                              QPen(QColor(0, 0, 0, 200)))
        self.m_verticalRuler = self.addLine(QLineF(0, 0, 0, self.height()),
                                            QPen(QColor(0, 0, 0, 200)))
        self.m_lineTo = self.addLine(QLineF(), QPen(QColor(0, 0, 0, 200)))
        self.m_horizontalRuler.setVisible(False)
        self.m_verticalRuler.setVisible(False)
        self.m_lineTo.setVisible(False)

        i = len(self.m_key_boxes)
        while i > 0:
            i -= 1

            self.m_key_boxes[i].setSize(QSizeF(0.0, 0.0))
            self.m_key_boxes[i].resetStatus()
            if not self.m_preserveVisibility:
                self.m_key_boxes[i].setHidden(False)

        self.m_hypertextList = []
        self.m_hypertextList.append(self.addRect(QRectF(),
                                                 QPen(QColor(0, 0, 0, 100)),
                                                 QBrush(QColor(225, 225, 225,
                                                               200))))

        self.m_hyperImage = self.addPixmap(QPixmap())
        self.m_hyperImage.setVisible(False)
        self.m_plot_group = []

    def updateModifiers(self) -> None:
        modifierMask = int(QApplication.keyboardModifiers()) >> 25
        if modifierMask != self.m_lastModifierMask:
            self.m_lastModifierMask = modifierMask
            self.m_eventHandler.postTermEvent(GE_modifier, 0, 0, modifierMask,
                                              0, self.m_widget)

    def positionText(self, item: QGraphicsItem, point: QPoint) -> None:
        item.setZValue(self.m_currentZ)
        self.m_currentZ += 1

        cx = 0.0
        cy = item.boundingRect().bottom() + item.boundingRect().top() / 2.0

        if self.m_textAlignment & Qt.AlignLeft:
            cx = item.boundingRect().left()
        elif self.m_textAlignment & Qt.AlignRight:
            cx = item.boundingRect().right()
        elif self.m_textAlignment & Qt.AlignCenter:
            cx = (item.boundingRect().right() + item.boundingRect().left()) / 2

        item.setTransformOriginPoint(cx, cy)
        item.setRotation(-self.m_textAngle)
        item.setPos(point.x() - cx, point.y() - cy)

    def setBrushStyle(self, style: int) -> None:
        fillpar = style >> 4
        fillstyle = style & 0xf

        self.m_currentBrush.setStyle(Qt.SolidPattern)
        self.m_currentFillStyle = fillstyle

        color = self.m_currentPen.color()

        if fillstyle == FS_TRANPARENT_SOLID:
            color.setAlphaF(fillpar / 100)
        elif fillstyle == FS_SOLID and fillpar < 100:
            fact = (100 - fillpar) / 100
            factc = 1.0 - fact

            if fact >= 0.0 and factc >= 0.0:
                color.setRedF(color.redF() * factc + fact)
                color.setGreenF(color.greenF() * factc + fact)
                color.setBlueF(color.blueF() * factc + fact)
        elif fillstyle == FS_TRANSPARENT_PATTERN or fillstyle == FS_PATTERN:
            self.m_currentBrush.setStyle(QtGnuplotBrushes[fillpar % 8])
        elif fillstyle == FS_EMPTY:
            color = self.m_widget.backgroundColor()
        self.m_currentBrush.setColor(color)

    def updateRuler(self, point: QPoint) -> None:
        if point.x() <= 0:
            self.m_horizontalRuler.setVisible(False)
            self.m_verticalRuler.setVisible(False)
            self.m_lineTo.setVisible(False)
            return

        pointF = QPointF(point) + QPointF(0.5, 0.5)
        self.m_horizontalRuler.setVisible(True)
        self.m_verticalRuler.setVisible(True)

        self.m_horizontalRuler.setPos(0, pointF.y())
        self.m_verticalRuler.setPos(pointF.x(), 0)

        line = self.m_lineTo.line()
        line.setP1(pointF)
        self.m_lineTo.setLine(line)

    def flushCurrentPolygon(self) -> None:
        if self.m_currentPolygon.size() < 2:
            self.m_currentPolygon.clear()
            return

        self.m_currentPolygon = self.clipPolygon(self.m_currentPolygon)

        if not self.m_inKeySample:
            self.m_currentPointsItem.addPolygon(self.m_currentPolygon,
                                                self.m_currentPen)
        else:
            self.flushCurrentPointsItem()
            path = QPainterPath()
            path.addPolygon(self.m_currentPolygon)
            brush = QBrush()
            brush.setStyle(Qt.NoBrush)
            pathItem = self.addPath(path, self.m_currentPen, brush)
            pathItem.setZValue(self.m_currentZ)
            self.m_currentZ += 1

        self.m_currentPolygon.clear()

    def flushCurrentPointsItem(self) -> None:
        if self.m_currentPointsItem.isEmpty():
            return

        self.m_currentPointsItem.setZValue(self.m_currentZ)
        self.m_currentZ += 1
        self.addItem(self.m_currentPointsItem)
        self.m_currentGroup.append(self.m_currentPointsItem)
        self.m_currentPointsItem = QtGnuplotPoints()

    def clipPolygon(self, polygon: QPolygonF,
                    checkDiag: bool = True) -> QPolygonF:
        if checkDiag:
            for i in range(1, polygon.size()):
                if polygon[i].x() != polygon[i - 1].x() and \
                   polygon[i].y() != polygon[i - 1].y():
                    return polygon

        for i in range(polygon.size()):
            polygon[i].setX(qRound(polygon[i].x() + 0.5) - 0.5)
            polygon[i].setY(qRound(polygon[i].y() + 0.5) - 0.5)

        return polygon

    def clipPoint(self, point: QPointF) -> QPointF:
        point.setX(qRound(point.x() + 0.5) - 0.5)
        point.setY(qRound(point.y() + 0.5) - 0.5)
        return point

    def clipRect(self, rect: QRectF) -> QRectF:
        rect.setTop(qRound(rect.top() + 0.5) - 0.5)
        rect.setBottom(qRound(rect.bottom() + 0.5) - 0.5)
        rect.setLeft(qRound(rect.left() + 0.5) - 0.5)
        rect.setRight(qRound(rect.right() + 0.5) - 0.5)
        return rect

    def sceneToGraph(self, axis: int, coord: float) -> float:
        if self.m_axisScale[axis] == 0.0:
            return 0

        result = self.m_axisMin[axis] + (coord - self.m_axisLower[axis]) / self.m_axisScale[axis]
        if self.m_axisLog[axis] > 0.0:
            result = math.exp(result * self.m_axisLog[axis])
        return result

    def update_key_box(self, rect: QRectF) -> None:
        if self.m_currentPlotNumber > len(self.m_key_boxes):
            # DEBUG Feb 2018 should no longer trigger
            # because m_key_box insertion is done in layer code for GEAfterPlot
            self.m_key_boxes.insert(self.m_currentPlotNumber - 1,
                                    QtGnuplotKeybox(rect))
        elif self.m_key_boxes[self.m_currentPlotNumber - 1].isEmpty():
            tmp = self.m_key_boxes[self.m_currentPlotNumber - 1].isHidden()
            self.m_key_boxes[self.m_currentPlotNumber - 1] = QtGnuplotKeybox(rect)
            self.m_key_boxes[self.m_currentPlotNumber - 1].setHidden(tmp)
        else:
            self.m_key_boxes[self.m_currentPlotNumber - 1] |= rect
