.. _runstatus:

.. highlight:: csh

*******************
Run state detection
*******************

Runs tree view is updated at the SOLPS-GUI startup with the following steps:
 1. GUI is opened with an empty Runs and Archive tree view. Difference
    between both tree views is purely logical and can be moved forth
    and back with :guilabel:`Archive` and :guilabel:`Restore` buttons
    at runtime.
 2. At start a thread starts scanning through the directory trees to
    quickly provide directories for tree view.
 3. Right after Step 2 finishes and shows the tree in *Runs* and *Archive*
    thread that scans each directory for presence of files and directories that
    can describe current directory state.
 4. Within the Step 3 static data is collected and filled in remaining columns
    of the tree views.
 5. Further changes to the tree view state are done by **run update**
    via network from batch processes to GUI status server that is
    listening on user specified port.

As described within the function ``retrieve_folder_status(directory)``
detection of the **run state** is extracted from several *log* and *status*
files. From these files the current state is further analysed for
running/crash state.

Detection of the running code status is done with the presence of
``b2mn.exe.dir`` subdirectory. However, if the directory is not
*fresh enough* (e.g. 1 minute without a change of any file inside),
we can mark the run as **CRASHED**. Otherwise we can safely assume
that the status is **running**.

----------------
Stopping the run
----------------

The graceful **stop** command line is::

    $ touch b2mn.exe.dir/.quit

The same effect is done by selecting the run in Runs tree view
and pressing :guilabel:`Stop` button.

----------------
Starting the run
----------------

Running locally is usually executed in ``csh`` command line with::

   $ b2run b2mn < input.dat >& run.log

The same effect is done by selecting the run in Runs tree view
and pressing :guilabel:`Start` button.

The run has already occurred if all the input files are older than
the output files. That's what the ``Makefile checks``. If it finds
that the "b2mn.prt" file is up to date, it does not restart the run.

.. TODO::

GUI can be enhanced to mimic b2run restart logic by checking if
the *input files* are newer than the *output files*.