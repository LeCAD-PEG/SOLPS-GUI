.. highlight:: csh

.. _install-howto:

======================
SOLPS GUI Installation
======================

:Author: Leon Kos


SOLPS GUI consist of the following components:

 - GUI writen in PyQt5 and Python3
 - ParaView with IMAS plugin (optional)
 - Gnuplot 5 and PyQt5 widget (optional)

System requirements
===================

The SOLPS GUI components are able to be built on Linux systems with low-end
hardware and graphics capabilities. It runs well on a virtual machine with
several GB of RAM and few processing cores.

The SOLPS GUI is developed with the latest version of libraries and tools
having in mind long-term building possibility. For older Linux systems based
on kernel 2.6.18 onwards we are providing build scripts that can compile and
install required software components not available on these systems.

The following typical setups are possible:

 1. SOLPS GUI is compiled locally on a Linux workstation or laptop.
 2. SOLPS GUI components are built and installed by sysadmin on a cluster
    with virtual X11 desktop (x2go, NX, X11VNC, ...) using environment modules.
 3. SOLPS GUI is used as a submodule under SOLPS-ITER and partially builds
    missing widgets, plugins or components not provided on a cluster or
    a standalone Linux system.

Software requirements
=====================

The SOLPS GUI requires the following software components to be provided on the
system:

 1. Python 3.x with the following non-default libraries:
     - sphinx
     - sphinx_rtd_theme
     - matplotlib
     - PyQt5
 2. ParaView 5.x compiled with Catalyst including
     - IMAS library for ParaView plugin
     - CMake 3.5+ 
 3. Gnuplot 5.x with
     - PyQt5 Gnuplot widget for better user experience under SOLPS GUI

Minimum GCC compiler version is 4.8.x to build above tools and libraries.
It is recommended that single GCC compiler toolchain is used for providing
above runtime software.

.. note::

   We strongly suggest to build the required SOLPS GUI software components
   by build scipts provided in SOLPS GUI top directory as they were tested
   many times and guarantee compatibility when compiling GUI widget
   and PyQt5 Gnuplot plugin.

