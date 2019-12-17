from PyQt5.QtWidgets import (QGraphicsItem, QStyleOptionGraphicsItem, QWidget,
                             QGraphicsPixmapItem, QAbstractGraphicsShapeItem,
                             QGraphicsRectItem)
from PyQt5.QtGui import (QPen, QPainter, QColor, QPixmap, QPainterPath, QFont,
                         QPolygonF, QBrush, QFontMetricsF)
from PyQt5.QtCore import QRectF, QPointF, Qt

import logging


class QtGnuplotPoint(QGraphicsItem):
    def __init__(self, style: int, size: float, pen: QPen,
                 parent: QGraphicsItem = None) -> None:
        super(QtGnuplotPoint, self).__init__(parent)
        self.m_pen = pen
        self.m_color = pen.color()
        self.m_style = style
        self.m_size = 3 * size

    def boundingRect(self) -> QRectF:
        return QRectF(QPointF(-self.m_size, -self.m_size),
                      QPointF(self.m_size, self.m_size))

    def paint(self, painter: QPainter, origin: QPointF,
              option: QStyleOptionGraphicsItem,
              widget: QWidget = None) -> None:

        # UNUSED OPTION WIDGET

        style = self.m_style % 15
        if style % 2 == 0 and style > 3:  # Filled points
            painter.setPen(self.m_color)
            painter.setBrush(self.m_color)
        else:
            painter.setPen(self.m_pen)
        self.drawPoint(painter, QPointF(0.0, 0.0), self.m_size, style)

    @staticmethod
    def drawPoint(painter: QPainter, origin: QPointF, size: float,
                  style: int) -> None:

        if style == -1:  # Dot
            painter.drawPoint(origin)
            return

        if style == 0 or style == 2:  # Plus or star
            painter.drawLine(origin + QPointF(0., -size),
                             origin + QPointF(0., size))
            painter.drawLine(origin + QPointF(-size, 0.),
                             origin + QPointF(size, 0.))
        if style == 1 or style == 2:  # Cross or star
            painter.drawLine(origin + QPointF(-size, -size),
                             origin + QPointF(size, size))
            painter.drawLine(origin + QPointF(-size, size),
                             origin + QPointF(size, -size))
        elif style == 3 or style == 4:  # Box
            painter.drawRect(QRectF(origin + QPointF(-size, -size),
                                    origin + QPointF(size, size)))
        elif style == 5 or style == 6:  # Circle
            painter.drawEllipse(QRectF(origin + QPointF(-size, -size),
                                       origin + QPointF(size, size)))
        elif style == 7 or style == 8:  # Triangle
            p = [origin + QPointF(0, -size),
                 origin + QPointF(0.866 * size, 0.5 * size),
                 origin + QPointF(-0.866 * size, 0.5 * size)]
            painter.drawPolygon(QPolygonF(p))
        elif style == 9 or style == 10:  # Upside down Triangle
            p = [origin + QPointF(0, size),
                 origin + QPointF(0.866 * size, -0.5 * size),
                 origin + QPointF(-0.866 * size, -0.5 * size)]
            painter.drawPolygon(QPolygonF(p))
        elif style == 11 or style == 12:  # Diamond
            p = [origin + QPointF(0, size),
                 origin + QPointF(size, 0),
                 origin + QPointF(0, -size),
                 origin + QPointF(-size, 0)]
            painter.drawPolygon(QPolygonF(p))
        elif style == 13 or style == 14:  # Pentagon
            p = [origin + QPointF(0, size),
                 origin + QPointF(size * 0.9511,  size * 0.3090),
                 origin + QPointF(size * 0.5878, -size * 0.8090),
                 origin + QPointF(-size * 0.5878, -size * 0.8090),
                 origin + QPointF(-size * 0.9511,  size * 0.3090)]
            painter.drawPolygon(QPolygonF(p))


class QtGnuplotClippedPixmap(QGraphicsPixmapItem):
    def __init__(self, clipRect: QRectF, pixmap: QPixmap,
                 parent: QGraphicsItem = 0) -> None:
        super(QtGnuplotClippedPixmap, self).__init__(pixmap, parent)
        self.m_clipRect = clipRect
        self.setFlags(self.flags() | QGraphicsItem.ItemClipsToShape)

    def shape(self) -> QPainterPath:
        p = QPainterPath()
        p.addRect(self.m_clipRect)
        return p


class QtGnuplotEnhancedFragment(QAbstractGraphicsShapeItem):
    def __init__(self, font: QFont, text: str,
                 parent: QGraphicsItem = 0) -> None:
        super(QtGnuplotEnhancedFragment, self).__init__(parent)
        self.m_font = font
        self.m_text = text

    def boundingRect(self) -> QRectF:
        metrics = QFontMetricsF(self.m_font)
        return metrics.boundingRect(self.m_text)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem,
              widget: QWidget = 0) -> None:
        # UNUSED OPTION AND WIDGET
        painter.setPen(self.pen())
        painter.setFont(self.m_font)
        painter.drawText(QPointF(0.0, 0.0), self.m_text)

    def width(self) -> float:
        metrics = QFontMetricsF(self.m_font)
        return metrics.width(self.m_text)


class QtGnuplotEnhanced(QGraphicsItem):
    def __init__(self, parent: QGraphicsItem = None):
        super(QtGnuplotEnhanced, self).__init__(parent)
        self.m_overprintMark = False
        self.m_overprintPos = None  # 0.0
        self.m_currentPos = QPointF()  # QPointF(0.0, 0.0)
        self.m_savedPos = QPointF()  # QPointF(0.0, 0.0)

    def boundingRect(self) -> QRectF:
        return self.childrenBoundingRect()

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem,
              widget: QWidget = None) -> None:
        # UNUSED
        pass

    def addText(self, fontName: str, fontSize: float, fontStyle: QFont.Style,
                fontWeight: QFont.Weight, base: float, widthFlag: float,
                showFlag: bool, overprint: int, text: str,
                color: QColor) -> None:

        if overprint == 1 and not self.m_overprintMark:
            self.m_overprintPos = self.m_currentPos.x()
            self.m_overprintMark = True

        if overprint == 3:
            self.m_savedPos = self.m_currentPos  # Save position
        elif overprint == 4:
            self.m_currentPos = self.m_savedPos  # Recall saved position

        logging.debug(f"Font {fontName}, Size {fontSize}")
        if isinstance(fontName, bytes):
            fontName = fontName.decode()
        font = QFont(fontName, fontSize)
        if fontName == '':
            font.setFamily('Sans')  # Use default/ Use previous ?

        font.setStyle(fontStyle)
        font.setWeight(fontWeight)
        font.setStyleStrategy(QFont.ForceOutline)  # pcf fonts die if rotated

        item = QtGnuplotEnhancedFragment(font, text, self)
        item.setPos(self.m_currentPos + QPointF(0., -base))

        if showFlag:
            item.setPen(color)
        else:
            p = QPen()
            p.setStyle(Qt.NoPen)
            item.setPen(p)

        if overprint == 2:
            x = self.m_overprintPos + self.m_currentPos.x()/2 - item.width()/2
            item.setPos(QPointF(x, -base))
            self.m_overprintMark = False

        if widthFlag and overprint != 2:
            self.m_currentPos += QPointF(item.width(), 0.0)


class QtGnuplotKeybox(QRectF):
    def __init__(self, rect: QRectF) -> None:
        super(QtGnuplotKeybox, self).__init__(rect)
        self.m_hidden = False
        self.m_statusBox = None

    def setHidden(self, state: bool) -> None:
        self.m_hidden = state
        if self.m_statusBox:
            self.m_statusBox.setVisible(self.m_hidden)

    def isHidden(self) -> bool:
        return self.m_hidden

    def showStatus(self, me: QGraphicsRectItem) -> None:
        logging.debug(f"showStatus {me}")
        self.m_statusBox = me
        self.m_statusBox.setVisible(self.m_hidden)

    def resetStatus(self) -> None:
        self.m_statusBox = None


class QtGnuplotPoints_PointData:
    z = -1
    point = None
    style = -1
    pointSize = 0.0
    pen = None


class QtGnuplotPoints_PolygonData:
    z = -1
    polygon = None
    pen = None


class QtGnuplotPoints_FilledPolygonData:
    z = 0
    polygon = None
    brush = None


class QtGnuplotPoints(QGraphicsItem):
    def __init__(self, parent: QGraphicsItem = None) -> None:
        super(QtGnuplotPoints, self).__init__(parent)

        self.m_points = []
        self.m_polygons = []
        self.m_filledPolygons = []
        self.m_boundingRect = QRectF()
        self.m_currentZ = 0

    def addPoint(self, point: QPointF, style: int, pointSize: float,
                 pen: QPen) -> None:
        data = QtGnuplotPoints_PointData()
        data.point = QPointF(point)  # Make a copy, otherwise it's a reference
        data.style = style
        data.pointSize = 3 * pointSize
        data.pen = QPen(pen)  # Make a copy, otherwise it's a reference
        data.z = self.m_currentZ
        self.m_currentZ += 1
        self.m_points.append(data)

        size = data.pointSize
        origin = data.point
        self.m_boundingRect = self.m_boundingRect.united(
            QRectF(origin + QPointF(-size, -size),
                   origin + QPointF(size, size)))

    def addPolygon(self, polygon: QPolygonF, pen: QPen) -> None:
        data = QtGnuplotPoints_PolygonData()
        data.polygon = QPolygonF(polygon)  # Make a copy, otherwise it's a reference
        data.pen = QPen(pen)  # Make a copy, otherwise it's a reference
        data.z = self.m_currentZ
        self.m_currentZ += 1
        self.m_polygons.append(data)
        self.m_boundingRect = self.m_boundingRect.united(
            data.polygon.boundingRect())

    def addFilledPolygon(self, polygon: QPolygonF, brush: QBrush) -> None:
        data = QtGnuplotPoints_FilledPolygonData()
        data.polygon = QPolygonF(polygon)  # Make a copy, otherwise it's a reference
        data.brush = QBrush(brush)  # Make a copy, otherwise it's a reference
        data.z = self.m_currentZ
        self.m_currentZ += 1
        self.m_filledPolygons.append(data)
        self.m_boundingRect = self.m_boundingRect.united(
            data.polygon.boundingRect())

    def isEmpty(self) -> bool:
        if len(self.m_points) or len(self.m_polygons) or \
           len(self.m_filledPolygons):
            return False
        return True

    def boundingRect(self) -> QRectF:
        return self.m_boundingRect

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem,
              widget: QWidget = None) -> None:
        # UNUSED OPTION WIDGET
        painter.setBrush(Qt.NoBrush)

        i = 0
        j = 0
        k = 0
        z = 0

        n_points = len(self.m_points)
        n_polygons = len(self.m_polygons)
        n_filled_polygons = len(self.m_filledPolygons)
        while i < n_points or j < n_polygons or k < n_filled_polygons:

            while i < n_points:
                point = self.m_points[i]
                if point.z != z:
                    break
                i += 1
                z += 1

                style = point.style % 15

                painter.setPen(point.pen.color())
                if style % 2 == 0 and style > 3:  # Filled points
                    painter.setBrush(point.pen.color())
                else:
                    painter.setPen(point.pen)
                    painter.setBrush(Qt.NoBrush)

                QtGnuplotPoint.drawPoint(painter, point.point, point.pointSize,
                                         style)
            painter.setBrush(Qt.NoBrush)

            while j < n_polygons:
                polygon = self.m_polygons[j]
                if polygon.z != z:
                    break
                j += 1
                z += 1

                painter.setPen(polygon.pen)
                painter.drawPolyline(polygon.polygon)

            while k < n_filled_polygons:
                filled_polygon = self.m_filledPolygons[k]

                if filled_polygon.z != z:
                    break

                k += 1
                z += 1

                pen = QPen(Qt.NoPen)
                brush = filled_polygon.brush

                if brush.style() == Qt.SolidPattern:
                    pen = brush.color()

                painter.setPen(pen)
                painter.setBrush(brush)
                painter.drawPolygon(filled_polygon.polygon)
