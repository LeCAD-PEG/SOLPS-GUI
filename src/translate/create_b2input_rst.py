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

def add_switch(node, prefix='', name_prefix='``'):
    global reST_text

    name = node.findtext('name')

    reST_text += prefix + name_prefix + name + name_prefix


    reST_text += prefix + get_default_and_type(node) + '\n'

    if node.find("description") != None:
        add_description(node, prefix)


def add_switchgroup(node):
    global reST_text

    name = node.findtext('name')
    reST_text += "``" + name + "``\n"
    for element in node.findall('switch'):
        add_switch(element, prefix='  - ', name_prefix='``')
    reST_text += '\n'
    add_description(node)




import sys
if sys.argv[1]:
    tree = etree.parse(sys.argv[1])
    root = tree.getroot()
else:
    sys.exit()


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
        body(category.attrib['name'], '=')

        for element in category:
            if element.tag == "switch":
                add_switch(element)
            elif element.tag == "switchgroup":
                add_switchgroup(element)

print(reST_text)