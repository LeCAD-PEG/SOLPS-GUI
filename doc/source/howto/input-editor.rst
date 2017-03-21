
.. _input-editor-howto:

.. highlight:: csh
   
==================
Input editor HOWTO
==================

:Author: Gregor Simič, University of Ljubljana

This howto describes how B2 and Eirene editors work and explains the structure
of b2input.xml.

Eirene editor
=============

The Eirene input file is basically lines and lines of values with almost no 
indicators for which parameters the values are. The Eirene editor helps the 
user by showing the description of parameters and the content of lines in the 
editor.

The eirene editor is a tree-view based editor for the eirene input file. It has
two windows, one with the tree-style displayed text and the second holds the 
help description.

The tree-style is used for easier navigation. While you navigate through the
lines the second window will tell you which parameters are on the line and if
you navigate into a line, it will show you the description of the parameter
that is behind a value in the line.

Currently the parameters are determined by reading the input file line by line.
There is no model that would auto-update itself if there are changes to flags
or parameters that influence on the structure of the input file.

The Eirene editor is capable of running in stand alone mode by passing the 
path of the input file to the Eirene editor .py file. e.g.:

.. code-block:: bash

    python3 eirene.py /PATH/TO/THE/INPUT/FILE

B2 editor
=========

The B2 editor is a plaintext editor with the addition of having tool tips for
parameters and switches for the b2 input files.

When a b2 input file is loaded it loads the tool tips for the file. The switches
and parameters are highlighted if they are described in the b2input.xml. Note
that the highlight apply is case sensitive, so a switch might not be 
highlighted but the highlight pop-up still shows up!

``b2input.xml`` schema
======================

For editing b2input.xml it is recommended to have an editor that uses ``TABS``
for indenting and handles markup languages well.

Recommended editors:
   - Emacs version 24+
   - Sublime Text 2/3
   - oXygen XML editor

**Emacs version 24+:**

It is an open source, lightweight, editor, well featured but has a steep 
learning curve at the beginning of usage.

Emacs is rich with key-commands, which provides high operability and control
over editing files.
   
Be sure to have package nxml installed, as b2input.xml has settings at the 
bottom.

   .. code-block:: xml

      <!--
          Local variables:
          indent-tabs-mode: t
          tab-width: 4
          mode: nxml
          eval: (adaptive-wrap-prefix-mode t)
          nxml-child-indent: 4
          nxml-attribute-indent: 4
          nxml-slash-auto-complete-flag: t
          End:
          To install adaptive-wrap do: M-x package-install RET adaptive-wrap RET
          eval: (visual-line-mode t)
      -->

Otherwise you have to manually set ``tab-width`` setting and adaptive wrappings
 for optimal editing.

**Sublime text 3:**

It is a visually and user friendly editor that comes with a lot of features.

You can install a package manager and add packages if needed, but it handles
XML files, and others, nicely on it's own.

**oXygen XML editor:**

It is a full-stack IDE studio for editing and verifying XML files. It also
comes with .xslt support so you can write and execute the 
xsl-transformations inside the editor.

It is rich in function so reading the manual is a must for optimal editing. The
only downside is that it has a license you must buy and it does not come cheap.

Pros and cons for the recommended editors:

- Emacs:
   - **Pros**:
      - Open source
      - Highly customizable
      - Lightweight
   - **Cons**:
      - Steep learning curve

- Sublime text:
   - **Pros**:
      - User friendly
      - Highly customizable
      - Lightweight
   - **Cons**:
      - Proprietary, but free to use

- oXygen XML editor:
   - **Pros**:
      - Robust when it comes to handling .XML files
      - Full stack IDE for .XML and .XSLT
   - **Cons**:
      - Expensive



b2input.xml is a file that contains the switches and parameters as well as the
description, category, default values and notes of them.

For indenting it uses tabs as ``\\t`` and not white spaces.

Switch block
------------

The element of a switch or parameter is:

.. code-block:: xml

   <switch>
       <name>Name of parameter or switch</name>
       <default>Default value</default>
       <type>The type of the parameter or switch</type>
       <note>***Optional***</note>
       <description>
           Text that describes the parameter or switch.
       </description>
   </switch>

When a group of switches contains the same description, a switchgroup
should be made:

.. code-block:: xml

   <switchgroup>
       <name>name of switchgroup</name>
       <description>
           the description of switches
       </description>
       <switch>
           <name>name of the switch</name>
           <type>type of the switch</type>
           <note>***Optional***</note>
       </switch>
       .
       .
       .
   </switchgroup>


Switches and switchgroup elements are contained in categories. The name of the
category is stored in the attribute of the category tag!
i.e.:

.. code-block:: xml

   <category name="name of category">
       <switchgroup>
       ...
       </switchgroup>
       ...

       <switch>
       ...
       </switch>
       ...
   </category>


Additional text for creating Fortran and other format files, are stored in
separate elements. There can be an arbitrary number of routine elements:

.. code-block:: xml

   <routine name="name of the fortran file">
       <purpose>Content of the purpose of the fortran file</purpose>
       <introduction name="Title of introduction">
           Introduction text
       <introduction>
   </routine>

All of the previous elements are stored in module element, which has an 
attribute ``name`` containing the name of the input file and ``type`` if the 
input file is a fortran namelist.

If the input file is not a fortran namelist, then the attribute ``type`` **must
not be added**.

Example of a module node:

.. code-block:: xml

   <module name="Name of module">
       <routine name="Fortran file 1">
           ...
       </routine>
       <category name="Category 1">
           ...
       </category>
       <category name="Category 2">
           ...
       </category>
   </module>

The root of the xml file contains all the modules.

.. code-block:: xml
    
   <b2>
       <module name="module 1">
       ...
       </module>
       <module name="module 2">
       </module>
   </b2>

The purpose of the XML is to have all modules input available for
translation into documentation, tooltips and source code.


Additionally you can add comments within the root element e.g.:

.. code-block:: xml

   <!-- Comment -->

But do not edit or add comments outside of the root element

Writing description in b2input.xml
==================================

Text describing parameters and switches is normal plain text with some format 
rules.

Indentation
-----------

It's important to repeat that each line of description starts with ``5 tabs`` 
or ``\t\t\t\t\t``. Having whitespaces instead of tabs will break the format in 
which the description will be showcased in solps-gui or documentation. e.g.:

.. code-block:: xml

   <b2>
       <module name="Name of the module">
           <category name="Name of a category">
               ...
               <switch>
                   <name>some name</name>
                   <default>...</default>
                   <type>some type</type>
                   <description>
                       This text is indented with 5 tabs exactly.
                   </description>
               </switch>
               ...
               <switchgroup>
                   <name>name of switchgroup</name>
                   <description>
                       This text is also indented with 5 tabs. This is a group
                       description for the switches in this switchgroup.
                   </description>
                   ...
                   <switch>
                       <name>name of the switch</name>
                       <default>some value</default>
                       <type>...</type>
                       <description>
                       In some cases when a switch contains additional descr-
                       iption which only matters to this particular switch 
                       then you indent it as well with only FIVE!! tabs.
                       </description>
                   </switch>
                   ...
               </switchgroup>
           ...
           </category>
       </module>
   </b2>

Special symbols handling
------------------------

The next step is handling special symbols, e.g.: ``LOGICAL OPERATORS`` and 
``MATH SYMBOLS``.

The reason for the rules is that the programs that are parsing the b2input.xml 
are sensitive to markup signs, e.g. ``>`` or ``<``. And these signs are of 
course used for logical statements.

Current rules list for symbols:

- ``&ge;`` instead of ``>=``
- ``&gt;`` instead of ``>``
- ``&lt;`` instead of ``<``
- ``&amp;`` instead of ``&``
- ``'`` instead of any quotes or fancy quotes.
- ``''`` instead of any double quotes or fancy quotes.

The next is a current list of rules for subscripts and superscripts:

- ``x<sup>2</sup>`` instead of ``$x^2$``
- ``x<sub>2</sub>`` instead of ``$x_2$``

The reason behind this is that in solps-gui qt can render html code and for 
generating documentation it is easier to handle markup instead of latex code.

Documentation generation
------------------------

For generating documentation [and solps-gui help files] we use a python and 
xslt programs to parse and create the desired format. I will only concentrate 
on generating documentation files as user should not meddle with xslt 
generators for solps-gui.

Currently there are two python files names ``b2cdci.py`` and ``b2cdcn.py`` that
generate ``b2cdci.F`` and ``b2cdcn.F`` respectively.

There can be some introduction or some explanation text that gives us a summary
of either some switches or a category of switches. For that you can use the 
following markups:

Routine markup
~~~~~~~~~~~~~~
This is currently used for adding a description to generate fortran .F files.
Again all descriptions have **five tabs** indentation.
An example from b2input.xml:

.. code-block:: xml

   <b2>
       ...
       ...
       <module name="b2.parameters" type="namelist">
           <routine name="b2cdcn">
               <purpose>
                   B2CDCN provides information about namelists of the b2 code.
                   No computation is performed in this routine. 

                   The namelists are listed in no particular order. Each description will begin with the file from which the code expects to read the namelist and its general purpose. Then, each namelist variable will be listed with its use and size.
               </purpose>
           </routine>
           ...
           ...
       </module>
       ...
       ...
   </b2>

The content of ``<purpose>`` holds the text for the introduction in the 
``b2cdcn.F`` file.