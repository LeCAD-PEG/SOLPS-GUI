

from directorplugin import DirectorPlugin
from solpsinputplugin import SolpsInputPlugin
from lineinputplugin import LineInputPlugin

from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection

if __name__ == '__main__':
    QPyDesignerCustomWidgetCollection.addCustomWidget(DirectorPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(SolpsInputPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(LineInputPlugin())
