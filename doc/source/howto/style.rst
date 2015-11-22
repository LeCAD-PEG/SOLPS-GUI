.. _tunneling-howto:

.. highlight:: csh

*****************
SOLPS-GUI Styling
*****************

:Author: Leon Kos

Changing default look of the GUI is usually a necessity and not really a
styling question. Qt library provides look-and-feel depending on the platform.
However, there are command line options that can be used to change the style
overall and tailoring each widget. If no style is specified, Qt will choose
the most appropriate style for the user's platform or desktop environment.
Changing the style::

    $ src/gui/solps.py -style windows

Other styles can be dependend on the platform availability at the time of
compilation:
 * motif
 * cleanlooks
 * plastique

Stylesheet can be be passed as a command line parameter as::

   $ src/gui/solps.py -stylesheet gnome.qss

where gnome.qss specifies

..  code-block:: xml

    QTreeView
    {
      font: 12px;
    }

Further details on styleshets are explainded in
http://doc.qt.io/qt-5.5/stylesheet.html
