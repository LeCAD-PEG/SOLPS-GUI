.. highlight:: csh

.. catalyst_:


=======================
Using ParaView Catalyst
=======================

With this tutorial we'll show how to instrument the SOLPS-ITER code with
*in situ* visualization with ParaView Catalyst. SOLPS-ITER code needs to be 
compiled and linked with ParaView Catalyst libraries. Benefits of running
with Catalyst are:

 1. Live visualization of all exposed fields and creation of visualization 
    pipeline that can substantially reduce amount of data written during
    the simulation.
 2. Pausing and creating breakpoints at the specified time step.
 3. Writing VTK files for later inspection of all variables and analysis 
    over time.
 4. Saving image files without live connection to ParaView for later 
    creation of animations.
 5. ParaView can connect/disconnect to/from running simulation at any time.
 6. ParaView can export Python CoProcessing script of the pipeline for 
    customized output.
 7. Designed visualization pipeline is preserved among ParaView quit/starts.

The following deficiencies should also be considered when using Catalyst:
 1. ParaView Catalyst listen on user provided network port that must be
    globally agreed among user currently using the cluster. 
 2. Python coprocesing script needs to be modified for correct network
    interface and port of the login/visualisation node where ParaView
    will be started for in situ analysis.
 3. Only one simulation can connect to ParaView at time. If several 
    simulations are using the same port then only the first will connect.
    The rest will continue to run but could not be instrumented.
 4. It is not possible to disconnect listening Catalyst in ParaView and 
    start listening on some other port number to allow quick switching
    between many running simulations. Recommended way is to quit ParaView
    and start over with :menuselection:`Catalyst --> Connect`

Basic Catalyst simulation
-------------------------
We will start the default In situ *live visualization* on `hpc-app.iter.org`
login node using only B2.5.


Co-Processing pipeline
----------------------

We will extend default co-processing script to include saving each
time step for later analysis and creation of animation.
