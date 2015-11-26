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

  