from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection
from imasdbplugin import IMASDBPlugin

if __name__ == '__main__':
    QPyDesignerCustomWidgetCollection.addCustomWidget(IMASDBPlugin())