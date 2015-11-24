.. _runstatus:


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
files. From these files the current state is detected after running/crash
detection.

Detection of the running code status is done with the presence of
``b2mn.exe.dir`` subdirectory. However, if the directory is not
*fresh enough* (e.g. 1 minute without a change of any file inside),
we can mark the run as **CRASHED**. Otherwise we can safely assume
that the status is **running**.
