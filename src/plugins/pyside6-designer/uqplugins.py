#!/usr/bin/env python3
"""Qt Designer plugins for the four UQ actors (group "SOLPS UQ").

    UQSetupActor --samplesReady--> UQRunsActor --runsFinished--> UQAnalysisActor
    UQAnalysisActor --outputsCollected/resultsReady--> UQPlotActor
"""

from PySide6.QtGui import QIcon
from PySide6.QtDesigner import QDesignerCustomWidgetInterface

from uq_setup import UQSetupActor
from uq_runs import UQRunsActor
from uq_analysis import UQAnalysisActor
from uq_plot import UQPlotActor
from optimizationplugin import _logo_pixmap


class UQPluginBase(QDesignerCustomWidgetInterface):
    """Common plugin code. Subclasses set widgetClass, objectName, module,
    displayName and description.
    """

    widgetClass = None
    objectName = ''
    module = ''
    displayName = ''
    description = ''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initialized = False

    def initialize(self, core):
        if self.initialized:
            return
        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        return self.widgetClass(parent)

    def name(self):
        return self.widgetClass.__name__

    def group(self):
        return "SOLPS UQ"

    def icon(self):
        return QIcon(_logo_pixmap)

    def toolTip(self):
        return self.description

    def whatsThis(self):
        return self.description

    def isContainer(self):
        return False

    def domXml(self):
        return (
            f'<ui language="c++" displayname="{self.displayName}">\n'
            f' <widget class="{self.name()}" name="{self.objectName}">\n'
            '  <property name="toolTip">\n'
            f'   <string>{self.description}</string>\n'
            '  </property>\n'
            ' </widget>\n'
            '</ui>\n'
        )

    def includeFile(self):
        return self.module


class UQSetupPlugin(UQPluginBase):
    widgetClass = UQSetupActor
    objectName = 'uqSetupActor'
    module = 'uq_setup'
    displayName = 'UQ Setup'
    description = 'Uncertain inputs and OpenTURNS sampling. Emits samplesReady(study).'


class UQRunsPlugin(UQPluginBase):
    widgetClass = UQRunsActor
    objectName = 'uqRunsActor'
    module = 'uq_runs'
    displayName = 'UQ Runs'
    description = 'Sample run directories, Slurm and b2fplasmf. Emits runsFinished(study).'


class UQAnalysisPlugin(UQPluginBase):
    widgetClass = UQAnalysisActor
    objectName = 'uqAnalysisActor'
    module = 'uq_analysis'
    displayName = 'UQ Analysis'
    description = "QoIs, PCE/Kriging and Sobol' indices. Emits resultsReady(study)."


class UQPlotPlugin(UQPluginBase):
    widgetClass = UQPlotActor
    objectName = 'uqPlotActor'
    module = 'uq_plot'
    displayName = 'UQ Plot'
    description = "Sobol' indices, histograms and scatter plots of a UQ study."
