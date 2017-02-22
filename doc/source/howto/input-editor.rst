
.. _input-editor-howto:

.. highlight:: csh
   
==============================
Editing B2.5 and Eierene HOWTO
==============================

:Author: Gregor Simič, University of Ljubljana

.. only:: html

   .. contents::


Introduction
============

This howto describes how b2 and eirene editors work and explains the structure
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

Editing b2input.xml schema
==========================

This is a .xml file that contains the switches and parameters as well as the
description, category, default values and notes of them.

For indenting it uses tabs as \\t and not white spaces.

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

The description is normal text. For special characters use hexcodes or symbols
instead. e.g.::

		&ge; instead of >=
		&gt; instead of >
		&lt; instead of <
		&amp; isntead of &
		&#39; insead of '
		&quot instead of "

The reason for this is that xslt are used for parsing and transforming the xml
files into other desired files. For this it does not tolerate arrows.

When a group of switches contains the same description, a switchgroup should be
made:

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
attribute containing the name of the b2 input file. e.g.:

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

The purpose of the xml is to have a 

Optional
--------

Additionally you can add comments within the root element e.g.:

.. code-block:: xml

	<!-- Comment -->

But do not edit or add comments outside of the root element