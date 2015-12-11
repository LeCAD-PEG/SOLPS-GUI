.. _submission-howto:

.. highlight:: csh

*************************
Run Submission HOWTO
*************************

:Author: Leon Kos

SOLPS-ITER is primarily scripted within ``tcsh`` shell. For run submission,
environment with all libraries paths on different sites needs to be
encapsulated.

The following SOLPS-ITER environments are available as of December 2015:

 * ASIPP
 * CCFE
 * default
 * ENEA
 * FZJ
 * GA
 * IFERC
 * IN-DA
 * IPP
 * IPR
 * ITER
 * ITM
 * JET
 * KEIO
 * KSTAR
 * LEUVEN
 * ORNL
 * PPPL
 * SWIP
 * UNKNOWN
 * WM

Different **job sumbission** methods (:abbr:`LSF (Load Sharing Facility)`,
:abbr:`SGE (Son of Grid Engine)`, PBS, TORQUE, ...), are available depending
on the cluster where the code is being run.

Scripts that ease submission are site dependent:
 * itersubmit
 * itmsubmit
 * jetsubmit
 * sgesubmit

and they all look for ``QSUB.*`` templates that should resist in
``${SOLPSTOP}/runs`` directories. Different runs can have additional
job submission options but ideally, single submit command in the directory
should be sufficient for a submission script to figure out run type such as:
  * standalone
  * coulped with EIRENE
  * compressed logs


For single workstation ``localsubmit`` can be::

    #!/usr/bin/env tcsh
    setenv SHELL `which tcsh` # needed for batch and atd
    cat << __EOF__ | batch
    setenv LD_LIBRARY_PATH "${LD_LIBRARY_PATH}"
    set msg="Started on `hostname` at `date`"
    update_solps_run_status \${msg}
    echo ${USER} ${PWD} \${msg} | nc -u -v -w 0 ${SOLPS_GUI_IP} ${SOLPS_GUI_PORT}
    if (-e input.dat) then
       time b2run ${argv} b2mn < input.dat >! run.log
    else
       time b2run ${argv} -s  b2mn >! run.log
    endif
    set msg="Finished on `hostname` at `date`"
    echo ${USER} ${PWD} \${msg} | nc -u -v -w 0 ${SOLPS_GUI_IP} ${SOLPS_GUI_PORT}
    update_solps_run_status \${msg}
    __EOF__

Described script uses ``batch`` command that submits the job to local ``atd``.
Make sure that you increase default 0.8 load average when configuring
``atd -l <load>`` to <load> = n-1 cores of your system. Otherwise,
just one job will start at the moment. Two environment variables,
``${SOLPS_GUI_IP}`` and ``${SOLPS_GUI_PORT}`` from *Settings* are injected
before job is submitted to ``batch``.
