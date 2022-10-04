.. _faq-index:

*****************************
  Frequently Asked Questions
*****************************

.. toctree::
   :maxdepth: 1



============================
Graphical User Interface FAQ
============================

.. only:: html

   .. contents::


.. highlight:: csh


.. General GUI Questions
.. =====================

How do I change the Date Time display in Tree view?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use environmental variable LC_TIME. For example by prepending in ``bash``::

    $ LC_TIME=fr_FR src/gui/solps.py

Of course, this can be set in your shell too by ``export`` or ``setenv``.

To see which locales are available on the system use::

    $ locale -a


GUI program starts, but a window never appears.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
I have tried to launch the SOLPS-GUI from the SOLPS-ITER environment.
However, in that case, the GUI program starts, but a window never appears.
If I go directly to the SOLPS-GUI directory in a new shell and launch from
there, after sourcing setupenv, it works fine. If you do::

  $ module unload fontconfig

before launching then solps-gui works.


A: PPySide uses system fontconfig libraries. SOLPS modules implants their own
to the ``LD_LIBRARY_PATH``.

Workaround may be::

  $ (setenv LD_PRELOAD /usr/lib64/libfontconfig.so.1 && python3 src/gui/solps.py)

Other ways are using the same compilers/libraries for Qt, PySide and SOLPS-ITER
or simply adding an alias or a GUI run script that removes offending libraries.
Note that SOLPS-GUI doesn't require any SOLPS-ITER environment for its
operation as it sources setup.csh and login shell setup for each group
of runs that have common ``SOLPSTOP``.

I am getting XQcbConnection errors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Errors such as::

   QXcbConnection: Failed to initialize XRandr
   QXcbConnection: XCB error: 172 (Unknown), sequence: 157, ...
   failed to get the current screen resources

are related to the fact that the SOLPS-GUI uses XCB rendering libraries on X11
that are replacing "old" Xlib libraries. *XRandr* handles multi-display
extensions that are unavailable on remote displays. XCB errors in rendering
are related to "old" display managers and are usually not harmful. Upgrade
your X11 display drivers on login node if serious having problems.

How do I change default HTML browser for solps_doc?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. note::

   "Modern" HTML browser with Javascript and SVG support 
   is needed to read the SOLPS GUI documentation online.
   *K Desktop Environment* (KDE) provided default 
   *Konqueror* browser is not sufficient!

For KDE3 open KDE Control Center in shell with ::

 $ kcontrol

Then select :menuselection:`KDE Components --> File Associations
--> text --> html" and move your browser to the top.`.

For KDE4 select :menuselection:`Kmenu --> Configure Desktop -->
Advanced --> File Assoc --> Text --> HTML` and move your browser to
the top of the preferences.

Another way for `solps_doc` alias is to replace `xdg-open` with the
explicit command such as::

  firefox --url <URL to index.html>

.. seealso:: 
   
   Other desktop environments (GNOME, XFCE4, FCE, 
   Cinnamon,...) may have similar file associations desktop
   setting. See 
   `How do I add acroread as default PDF viewer for ParaView help?`_
   too.


============
ParaView FAQ
============


How do I add acroread as default PDF viewer for ParaView help?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Default PDF viewer for xdg-open can be obtained by::

   $ xdg-mime query default application/pdf

If there is no system ``/usr/share/applications/acroread.desktop`` file
one can create ``${HOME}./local/share/applications/acroread.desktop`` with
the following contents::

   [Desktop Entry]
   Name=Adobe Reader 9
   MimeType=application/pdf;application/vnd.fdf;application/vnd.adobe.pdx;application/vnd.adobe.xdp+xml;application/vnd.adobe.xfdf;
   Exec=acroread
   Type=Application
   GenericName=PDF Viewer
   Terminal=false
   Icon=AdobeReader9
   Caption=PDF Viewer
   X-KDE-StartupNotify=false
   Categories=Application;Office;Viewer;X-Red-Hat-Base;
   InitialPreference=9


and change default PDF viewer with::

   $ xdg-mime default acroread.desktop application/pdf

.. seealso:: `How do I change default HTML browser for solps_doc?`_


              
