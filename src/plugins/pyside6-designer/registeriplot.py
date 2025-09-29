from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection
from iplotplugin import IPlotPlugin

if __name__ == '__main__':
    QPyDesignerCustomWidgetCollection.addCustomWidget(IPlotPlugin())