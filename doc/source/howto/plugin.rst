.. _plugin-howto:

.. highlight:: csh

======================
SOLPS-GUI Plugin HOWTO
======================

:Author: Leon Kos

.. topic:: Abstract

   Creation of custom plugins written in C++ can extend SOLPS-GUI functionality
   and allow non-expert GUI programmers to easily configure dashboard with
   provided **Qt Designer** tool. Here we describe all non-trivial steps to
   create *custom PyQt plugins* that can be used in *Qt designer* and
   controlled with Python through Qt signal/slot mechanism.

Introduction
============

Dashboard is a place where user should be able to simply put widgets that are
used to monitor and analyse simulation runs. Dashboard configuration should be
extensible and easy enough for regular user to create own layout for the scope
of the work that dashboard can cover. SOLPS-GUI uses
`Qt widgets <http://www.qt.io>`_ for user interface programmed in Python and
`PyQt5 <http://sourceforge.net/projects/pyqt>`_  bindings that are easy enough
when using *standard* Qt widgets. SOLPS-GUI is designed with Qt tool
`designer <http://doc.qt.io/qt-5/qtdesigner-manual.html>`_. With the
** Qt designer** user can configure its own functionality and write appropriate
actions by extending Python code. Therefore, no GUI programming is needed for
simple tasks or look-and-feel reconfiguration. Simple tasks are adding a button
and creating accompaniying Python action code. For example, with added
*Push button* named ``pushButtonMyAction`` in *Qt Designer* the corresponding
button response routine is then placed in main window class as:

.. code-block:: python

    @pyqtSlot()
    def on_pushButtonMyAction_clicked(self):
        print('My actions follow.')

Longer tasks will need creation of a separate ``QThread`` to prevent GUI
freeze when Python code is executing.

Complex layout with several widgets that are usually combination of *input*
and *display* widgets require more coding.

Python Qt Designer plugins
==========================

If there are requests for many similar widgets to be placed on the dashboard
then it is reasonable to create a *composite* or *derived* widget [1]_ that
can be reusable with other users. It should be noted that such *custom widgets*
need to be available within the *Qt Designer* to be truly usable with
*drag and drop*.

PyQt provides a *Designer plugin loader* that allows writting *custom widgets*
in Python and can be used in for the dashboard. For more details on such Python
custom widgets for the *Qt designer* see
`Using Python Custom Widgets in Qt Designer
<https://wiki.python.org/moin/PyQt/Using_Python_Custom_Widgets_in_Qt_Designer>`_
wiki page [2]_, PyQt ``examples/designer/plugins`` source package and
PyQt5 tutorial [3]_. For each *custom widget* there needs to be created
accompanying Qt Designer plugin that follows requirements for inclusion and
provide information such as *widget group*, *icon*, *default values* for its
properties. Therefore, usually two directories are created:

 * ``widgets`` with custom widgets code, and
 * ``plugins/designer`` Qt Designer code that describe each widget.
   Directory containing these .py files is pointed with ``PYQTDESIGNERPATH``
   environment variable for Python designer loader to load them at startup.
   Plugin loader requires that the name of plugin must glob to ``*plugin.py``.
   For example: ``gnuplotplugin.py``.

Custom widget code needs to be visible to Qt Designer too by installing them
into ``site-packages`` or with the usual ``PYTHONPATH`` environment variable.
The same ``PYTHONPATH`` is needed by the GUI to import the widgets on
Dashboard where users are supposed to configure layout of these widgets.

When creating container plugin that includes other widgets one needs to create
designer extension that is somewhat more complex. However, this is usually not
needed and custom widget can be developed by inheriting top most widget
(eg. QTabWidget for input files editing) and do the widget initialisation on
runtime by calling setup routine or signaling usual operation.

.. note::
   On *OS X* plugin loader needs to be re-compiled with absolute path specified
   for ``PYTHON_LIB`` define in ``Makefile`` to load Python interpreter
   correctly.

C++ binding for PyQt
====================

For Qt display widgets or other processing in C++ one needs to prepare Python
bindings for C++ library that can be included in PyQt5 code. Although there are
general purpose language wrappers such as `SWIG <http://www.swig.org>`_ that
allow C and C++ code to Python, PyQt uses SIP [4]_ that provides binding of Qt
signal/slot mechanism not available with other "wrappers". Process of creating
Python module that allows inclusion of C++ code consists of the following
steps:

 1. C++ code in is encapsulated with ``QObject`` or derived classes such as
    ``QWidget``.
 2. Shared library is build by ``Makefile`` that was created from ``qmake``
    project file.
 3. SIP file needs to be writted describing C++ code for Python bindings
 4. ``configure.py`` file needs to be updated with details of the files used
    for the library. ``configure.py`` is a *boilerplate code* from
    `QScintilla2 <http://riverbankcomputing.com/software/qscintilla/download>`_
    project with clearly marked implementation sections tah needs to be
    updated.
 5. Another ``Makefile`` is generated by ``configure.py`` along with other
    files that will allow building of wrapped C++ code for Python bindings.
    Running ``make`` and then ``make install`` will create and install complete
    Python module that can be reused in Python code in the same way as other
    PyQt modules.

It should be noted that above steps create a *custom* C++ code for Python and
not a plugin for Qt Designer.

Minimal C++ to PyQt example
---------------------------

The following *Hello, SOLPS* example can be used to describe previous steps
with files and a resulting test in Python. The example from SIP tutorial [5]_
for PyQt4  is upgraded here for PyQt5 and has the following directory
structure::

 hello -+
        +- hello.h
        +- hello.cpp
        +- configure.py
        +- hello_test.py


Building the widget
^^^^^^^^^^^^^^^^^^^

.. code-block:: c++
   :caption: hello.h
   :name: hello-h

    // Define the interface to the hello library.
    #include <qlabel.h>
    #include <qwidget.h>
    #include <qstring.h>

    class Hello : public QLabel {
        // This is needed by the Qt Meta-Object Compiler.
        Q_OBJECT

    public:
        Hello(QWidget *parent = 0);

    private:
        // Prevent instances from being copied.
        Hello(const Hello &);
        Hello &operator=(const Hello &);
    };
    #if !defined(Q_OS_WIN)
    void setDefault(const QString &def);
    #endif

.. code-block:: c++
   :caption: hello.cpp

    #include "hello.h"
    #include "stdio.h"

    Hello::Hello(QWidget *parent):QLabel(parent)
    {
        printf("Hello, SOLPS\n");
    }

    Hello::Hello(const Hello &)
    {

    }

    Hello &Hello::operator=(const Hello &)
    {
        return *this;
    }

.. code-block:: guess
   :caption: hello.sip

   // Define the SIP wrapper to the hello library.
    %Module hello

    %Import QtWidgets/QtWidgetsmod.sip


    class Hello : public QLabel {

    %TypeHeaderCode
    #include <hello.h>
    %End

    public:
        Hello(QWidget *parent /TransferThis/ = 0);

    private:
        Hello(const Hello &);
    };

To prepare build files ``configure.py`` needs to be edited and run with::

    $ python3 configure.py --verbose
    $ make
    $ make install

For complete options usual ``python3 configure --help | less`` can be used.
Installed widget is placed under Python's ``site-packages/PyQt5`` directory.
To verify if the module hello.so has all shared libraries referenced issue::

    $ ldd -r hello.so

Undefined symbols may be fixed by adding missing library with ``-l`` in
the ``Makefile`` generated.

.. rubric:: References

.. [1] http://www.mail-archive.com/pyqt@riverbankcomputing.com/msg17893.html
.. [2] http://wiki.python.org/moin/PyQt/Using_Python_Custom_Widgets_in_Qt_Designer
.. [3] http://pyqt.sourceforge.net/Docs/PyQt5/designer.html#writing-qt-designer-plugins
.. [4] http://www.riverbankcomputing.com/software/sip
.. [5] http://pyqt.sourceforge.net/Docs/sip4/using.html#a-more-complex-c-example

