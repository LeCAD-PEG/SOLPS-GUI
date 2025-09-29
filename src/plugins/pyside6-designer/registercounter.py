from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection
from counter import Counter

# Set PYSIDE_DESIGNER_PLUGINS to point to this directory and load the plugin

TOOLTIP = "Counter for testing interactivity and timing"
DOM_XML = f"""
<ui language='c++' displayname='Counter'>
    <widget class='Counter' name='counter'>
        <property name="interval" stdset="0">
            <number comment='Time between intervals'
             extracomment='Integer describes miliseconds'>100</number>
        </property>
        <property name='toolTip'>   
                <string>{TOOLTIP}</string>
        </property>
        <property name="max_steps">
            <number>1000</number>
        </property>
        <property name="checkpoint_interval">
            <number>5</number>
        </property>
    </widget>
</ui>
"""
# See qttools/src/designer/src/components/formeditor/formeditor.qrc
ICON=":/qt-project.org/formeditor/images/widgets/lcdnumber.png"

if __name__ == '__main__':
    QPyDesignerCustomWidgetCollection.registerCustomWidget(Counter, module="counter", group='Custom',
                                                           tool_tip=TOOLTIP, xml=DOM_XML, icon=ICON)    