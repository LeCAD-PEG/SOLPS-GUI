# Set PYSIDE_DESIGNER_PLUGINS to point to this directory and load the plugin
from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection
{% if simple_actor %}
from {{ name }} import {{  class_name }}
import pdsicons

DOM_XML = f""" {{ dom_xml }}"""

# See qttools/src/designer/src/components/formeditor/formeditor.qrc
#ICON=":/qt-project.org/formeditor/images/widgets/lcdnumber.png"
ICON="{{ icon_path }}" 
# TODO Use generator to load resources and select icon from resources
{% else %}
from {{ name }}plugin import {{ class_name }}Plugin
{% endif %}
if __name__ == '__main__':
    {% if simple_actor %}
    QPyDesignerCustomWidgetCollection.registerCustomWidget({{ class_name }}, module='{{ name }}', group='{{ group }}',
                                                           tool_tip='{{ toolTip }}', xml=DOM_XML, icon=ICON)
    {% else %}
    QPyDesignerCustomWidgetCollection.addCustomWidget({{ class_name }}Plugin())
    {% endif %}
