tocdepth: 2


==========================
Graphic User Interface FAQ
==========================

.. only:: html

   .. contents::


.. highlight:: csh


General GUI Questions
=====================

How do I change the Date Time display in Tree view?
===================================================

Use environmental variable LC_TIME. For example by prepending in ``bash``::

    $ LC_TIME=fr_FR src/gui/solps.py

Of course, this can be set in your shell too by ``export`` or ``setenv``.

To see which locales are available on the system use::

    $ locale -a
