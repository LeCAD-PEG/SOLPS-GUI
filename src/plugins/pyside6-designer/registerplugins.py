from directorplugin import DirectorPlugin
from solpsinputplugin import SolpsInputPlugin
from lineinputplugin import LineInputPlugin
from archiveRunDirViewplugin import archiveRunDirViewPlugin
from b2plotplugin import B2plotPlugin
from carreplugin import CarrePlugin
from divgeoplugin import DivGeoPlugin
from getIDSplugin import getIDSplugin
from gnuplotplugin import GnuplotPlugin
from initializeRunplugin import RunPlugin
from logplugin import LogPlugin
from putIDSplugin import putIDSplugin
from runDirViewplugin import RunDirViewPlugin
from scriptplugin import ScriptWidgetPlugin
from solpsplotsplugin import SolpsPlotsPlugin
from tcshplugin import TcshWidgetPlugin
from triangplugin import TriangPlugin
from edgeprofilesplugin import EdgeProfilesPlugin
from tangentplugin import TangentPlugin
from adjointplugin import AdjointPlugin
from optimizationplugin import OptimizationPlugin

from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection

if __name__ == '__main__':
    QPyDesignerCustomWidgetCollection.addCustomWidget(DirectorPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(SolpsInputPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(LineInputPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(archiveRunDirViewPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(B2plotPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(CarrePlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(DivGeoPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(getIDSplugin())  
    QPyDesignerCustomWidgetCollection.addCustomWidget(GnuplotPlugin())  
    QPyDesignerCustomWidgetCollection.addCustomWidget(RunPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(LogPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(putIDSplugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(RunDirViewPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(ScriptWidgetPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(SolpsPlotsPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(TcshWidgetPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(TriangPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(EdgeProfilesPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(TangentPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(AdjointPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(OptimizationPlugin())
