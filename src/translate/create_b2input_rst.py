from __future__ import print_function

import xml.etree.ElementTree as etree
from xml.etree.ElementTree import tostring
import textwrap
from itertools import chain

greek_pattern = r"\&([A-z]+)\;"
import re

def body(string, c, with_outline=False):
    global reST_text
    if with_outline:
        reST_text += len(string) * c + '\n'
    reST_text += string + '\n'
    reST_text += len(string) * c + '\n'

def dedent(description):
    trim_start = 0  # Remove any leading newlines that affects dedent
    while trim_start < len(description) and description[trim_start] == '\n':
        trim_start += 1
    description = textwrap.dedent(description[trim_start:])
    return description

def get_default_and_type(node):
    second_line = ''
    switch_type = node.findtext('type')
    if switch_type: 
        second_line = '    type: ``' + switch_type + '``'

    default = node.findtext('default')
    if default:
        second_line += '    default: ``' + default + '``'

    return second_line

def stringify_children(node):
    if node != None:
        parts = ([node.text] +
                list(chain(*([tostring(c).split()[0], c.tail] for c in node.getchildren()))) +
                [node.tail])
        # filter removes possible Nones in texts and tails
        return ''.join([i.decode() if type(i) == bytes else i for i in filter(None, parts)])
    else:
        return ''

def extract(string, start, end):
    output = []
    for el in string.split(start)[1:]:
        output.append(el.split(end)[0])
    return output

def get_description(node):
    description = stringify_children(node.find('description'))
    description = description.replace('_', '\_')
    description = description.replace('*', '\*')
    if description:
        # Replace all <sub>, <sup>,...

        if "<sub>" in description:
            extracted_text = extract(description, "<sub>", "</sub>")
            description = description.replace('<sub>', '`_')
            description = description.replace('</sub>', '`')

            for argument in extracted_text:
                if len(argument.split()) > 1:
                    description.replace(argument, '{'+argument+'}')

        if "<sup>" in description:
            extracted_text = extract(description, "<sup>", "</sup>")
            description = description.replace('<sup>', '^')
            description = description.replace('</sup>', '`')

            for argument in extracted_text:
                if len(argument.split()) > 1:
                    description = description.replace(argument, '{'+argument+'}')
        greek_words = re.findall(greek_pattern, description)
        for word in greek_words:
            description.replace('&'+word+';', '\\' + word)


    return dedent(description)

def add_description(node, prefix=''):
    global reST_text

    indent = 0
    description = get_description(node)
    start = 1
    for line in description.splitlines():
        if line.startswith(' ') or line.startswith('\t'):
            if start:
                reST_text += '\n'
                start = 0
            reST_text += '    |' + line + '\n' 
        else:
            if start == 0:
                reST_text += '\n'
                start = 1
            reST_text += '    ' + line.lstrip() + '\n' 

def add_switch(node, prefix='', name_prefix='``', index=True):
    global reST_text


    name = node.findtext('name')    
    
    if index:
        reST_text += ".. index:: "   + name + "\n\n"

    reST_text += prefix + name_prefix + name + name_prefix


    reST_text += prefix + get_default_and_type(node) + '\n'

    if node.find("description") != None:
        add_description(node, prefix)


def add_switchgroup(node):
    global reST_text

    name = node.findtext('name') 
    sub_names = [e.findtext("name") for e in node.findall('switch')]



    reST_text += ".. index:: "+ name + '\n\n'
    reST_text += ".. index:: " + ", ".join(sub_names) + "\n.. c\n\n"
    reST_text += "``" + name + "``\n\n"

    for element in node.findall('switch'):
        add_switch(element, prefix='  - ', name_prefix='``', index=False)
        if reST_text[-2] != "\n":
            reST_text += '\n'
    reST_text += '\n'

    add_description(node)


    reST_text += ".. index::\n"
    for sub_name in sub_names:
        reST_text += "   single: " + name + "; " + sub_name + '\n'
    reST_text += '\n\n'




import sys

try:
    xml_name = sys.argv[1]
    dtd_name = sys.argv[2]
except Exception as e:
    sys.exit()

xml_entities = '<!ENTITY % symbols SYSTEM "xhtml-symbol.ent" > %symbols;'

f = open(xml_name, 'r')
xml_text = f.read()
f.close()

# Inserting DTD entities inside xml
f = open(dtd_name, 'r')
dtd_text = f.read()
f.close()


text_to_process = xml_text.replace(xml_entities, dtd_text)
f = open('test.xml', 'w')
f.write(text_to_process)
f.close()
print(text_to_process)
tree = etree.ElementTree(etree.fromstring(text_to_process))

root = tree.getroot()



head = 'B2.5 input'
reST_text = """.. _b2input:

"""

body(head, '#', with_outline=True)
reST_text += """

.. highlight:: csh

.. solps-gui-switches:


.. note::
	
	This is a generated reST file from b2input.xml. 
	It covers switches and parameters.

.. role:: latex(raw)
   :format: latex\n\n"""

for module in root:
    body(module.attrib['name'], '*', with_outline=True)

    for category in module.findall('category'):


        reST_text += ".. index:: " + category.attrib['name'] + "\n\n"
        reST_text
        body(category.attrib['name'], '=')
        names = []
        for element in category:
            
            if element.tag == "switch":
                names.append(element.findtext('name'))
                add_switch(element)
                if reST_text[-2] != '\n':
                    reST_text+='\n'
            elif element.tag == "switchgroup":
                names.append(element.findtext('name'))
                add_switchgroup(element)


        reST_text += ".. index:: \n"
        for name in names:
            reST_text += "   single: " + category.attrib['name'] +'; '+ name + '\n'

        reST_text += "\n"


print(reST_text)