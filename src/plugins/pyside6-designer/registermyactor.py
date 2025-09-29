# Set PYSIDE_DESIGNER_PLUGINS to point to this directory and load the plugin
from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection

from myactor import MyActor
import pdsicons

DOM_XML = f""" <ui language='c++' displayname='My Actor'>
    <widget class='MyActor' name='myactor'>
        <property name='geometry'>
            <rect>
                <width>300</width>
                <height>200</height>
            </rect>
        </property>
        <property name='pulse'>
            <string notr='true' comment='(shot, run, usename, database, backend)'
            extracomment='Tuple of IDS parameters'>(130012, 2, 'public', 'ITER', 12)</string>
        </property>
        <property name='title'>
            <string notr='true' comment='Text for widget title.'
            extracomment='Add this to widget title'>My Actor</string>
        </property>
        <property name='button'>
            <string notr='true' comment='Title for Start button'
            extracomment='Add this to button'>START</string>
        </property>
        <property name="show_log">
            <bool>true</bool>
        </property>
        <property name="show_button">
            <bool>true</bool>
        </property>
        <property name="show_title">
            <bool>true</bool>
        </property>
        <property name='toolTip'>	
                <string></string>
        </property>
        <property name='whatsThis'>	
                <string>This actor is part of SOLPS workflow</string>
        </property>
    </widget>
</ui>"""

# See qttools/src/designer/src/components/formeditor/formeditor.qrc
#ICON=":/qt-project.org/formeditor/images/widgets/lcdnumber.png"
ICON=":/qt-project.org/formeditor/images/widgets/progress.png" 
# TODO Use generator to load resources and select icon from resources

if __name__ == '__main__':
    
    QPyDesignerCustomWidgetCollection.registerCustomWidget(MyActor, module='myactor', group='Custom',
                                                           tool_tip='', xml=DOM_XML, icon=ICON)
    