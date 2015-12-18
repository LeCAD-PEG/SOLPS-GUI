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


A: PyQt uses system fontconfig libraries. SOLPS modules implants their own
to the ``LD_LIBRARY_PATH``.

Workaround may be::

  $ (setenv LD_PRELOAD /usr/lib64/libfontconfig.so.1 && python3 src/gui/solps.py)

Other ways are using the same compilers/libraries for Qt, pyqt and SOLPS-ITER
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