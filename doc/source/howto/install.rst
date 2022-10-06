.. highlight:: sh

.. _install-howto:

======================
SOLPS GUI Installation
======================

:Author: Leon Kos


SOLPS GUI consist of the following components:

 1. GUI writen in Python3 using PySide6 library
 2. ParaView with Catalyst and IMAS plugin (optional)
 3. Gnuplot5 with Qt terminal and PySide6 widget (optional)

Essentially, only the first component is needed for running SOLPS GUI and
in principle does not need to be compiled at all if the system provides
Python 3 and PyQt library. However, it turns out that these run-time tools
requirements are not always easily satisfied. To remedy these difficulties
we are providing build scripts written in (ba)sh shell that are capable of
building the missing components by a single command line.

On supported systems these scripts should build all missing libraries
without a problem by downloading the sources from internet, unpacking,
patching, configuring, building and installing into *staging* directory.
Standalone users and system administrators should be able to use these
*shell* scripts, residing in the project top directory, to build required
components for system wide installation or personal (standalone) use. As
always, it is recommended that system administrators build these tools in
order to save the time of the users and machine.

On untested systems the build scripts can be used mostly unalterred as many
of the configuration parameters can be specified in the command line just
before launching the script. It is advised that specific site reqirements
are then added into site-specific section of the script that override
default configuration variables without the need of specifying them in the
command line in future runs and thus recording this *tweaks* as build
instructions.

Optional components (ParaView, Gnuplot QT) are usually not provided on the
system in a correct manner as they are application specific with many
configuration options possible and not suited for use in the SOLPS GUI
framework.

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
     - PySide6
 2. ParaView 5.x compiled with Catalyst including
     - IMAS library for ParaView plugin
     - CMake 3.5+
 3. Gnuplot 5.x with
     - PySide6 Gnuplot widget for better user experience under SOLPS GUI

Minimum GCC compiler version is 4.8.x to build above tools and libraries.
It is recommended that single GCC compiler toolchain is used for providing
above runtime software.

.. note::

   We strongly suggest to build the required SOLPS GUI software components
   by build scripts provided in SOLPS GUI top directory as they were tested
   many times and guarantee compatibility when compiling GUI widget
   and PySide6 Gnuplot plugin.

=======================
SOLPS-ITER installation
=======================

For destop compilation SOLPS-ITER provides `SETUP/easbuild-local.sh` script
that allows easy building of required SOLPS-ITER module replicating ITER
cluster environment including SLURM submission scripts.

.. code-block:: 

    SETUP/easybuild-local.sh [OPTION... | easybuild_command...]

      --help                prints and opens this manual, then EasyBuild help
      --imas-foss           builds IMAS with foss-2020b toolchain
      --imas-foss install   installs IMAS and module
      --intel               build INTEL modules and toolchain
      --imas-intel clean    cleans IMAS repository before rebuilding
      --imas-intel          builds IMAS with INTEL toolchain
      --imas-intel install  installs IMAS and module built with INTEL
      --imas                builds default CentOS-8 IMAS built with GCC and INTEL
      --imas install        installs IMAS CentOS-8 module built with GCC and INTEL
      --imas-apps           builds all IMAS applications

    ENVIRONMENT variables:

      TAG_DD                   IMAS data dictionary version
      TAG_AL                   IMAS access layer version
      EASYBUILD_PREFIX         Software installation directory prefix
      EASYBUILD_MODULES_TOOL   Modules tool (Lmod, EnvironmentModules)
      EASYBUILD_MODULE_SYNTAX  Tcl or Lua syntax for modulefiles generated
      HTTP_AUTH_BEARER         Personal token for downloading of ITER GIT sources



We also provide scripts under ``package/`` for building the SOLPS-ITER suite along 
with it's required packages. Some of the requirements are written in the :file:`README.md`. 
For others, scripts are written that download, compile and install the code. At the
end of each package compilation, module files are generated and are, by
default, written into ``solps-gui/modules`` directory.

To compile the SOLPS-ITER suite, run the following command from the solps-gui
folder::

    cd solps-gui
    make solps-iter # It may take several hours


