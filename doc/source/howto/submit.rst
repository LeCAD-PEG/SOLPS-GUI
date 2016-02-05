.. highlight:: csh

.. _submission-howto:

====================
Run Submission HOWTO
====================

:Author: Leon Kos

SOLPS-ITER is primarily scripted within ``tcsh`` shell. For run submission,
environment with all libraries paths on different sites needs to be
encapsulated.

The following SOLPS-ITER environments are available as of December 2015:

 * ASIPP, CCFE,  default, ENEA, FZJ, GA, IFERC, IN-DA, IPP, IPR, ITER,
   ITM, JET, KEIO, KSTAR, LEUVEN, ORNL, PPPL, SWIP, UNKNOWN WM

Different **job submission** methods (:abbr:`LSF (Load Sharing Facility)`,
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

Local submission
^^^^^^^^^^^^^^^^

For a single workstation ``localsubmit`` can be::

    #!/usr/bin/env tcsh
    setenv SHELL `which tcsh` # needed for batch and atd
    cat << __EOF__ | batch
    setenv LD_LIBRARY_PATH "${LD_LIBRARY_PATH}"
    set msg="Started on `hostname` at `date`"
    update_solps_run_status \${msg}
    echo ${USER} ${PWD} \${msg} | nc -u -w 0 ${SOLPS_GUI_IP} ${SOLPS_GUI_PORT}
    if (-e input.dat) then
       time b2run ${argv} b2mn < input.dat >! run.log
    else
       time b2run ${argv} -s  b2mn >! run.log
    endif
    set msg="Finished on `hostname` at `date`"
    echo ${USER} ${PWD} \${msg} | nc -u -w 0 ${SOLPS_GUI_IP} ${SOLPS_GUI_PORT}
    update_solps_run_status \${msg}
    __EOF__

Described script uses ``batch`` command that submits the job to local ``atd``.
Make sure that you increase default 0.8 load average when configuring
``atd -l <load>`` to <load> = n-1 cores of your system. Otherwise,
just one job will start at the moment. Although ``localsubmit`` is primarily
intended for single users, it can handle multi-users without significantly
impact regular work as it will not go over the "system" specified load.
Results of the ``localsubmit`` diadnostic output can be read by system
``mail``. If *mail* is not desired then all ``b2mn`` output should be
redirected with ``>&!`` instead of just ``>!`` and then empty mails will
not be sent.

Two environment variables, ``${SOLPS_GUI_IP}`` and ``${SOLPS_GUI_PORT}``
from *Settings* are injected by the GUI before the job is submitted
to ``batch``.

In the above example handling of environmental variables needs to be taken care
of. All variables escaped with backslash (``\${.}``) are not evaluated at the
time of submission. Whereas the rest (``${.}``) are replaced before they arrive
to ``atd``. Although majority of environmental variables are passed to ``atd``
and restored later at the time of execution, there are some exceptions. Most
notable is ``LD_LIBRARY_PATH``. We also need to enforce that the current
submitting shell (*tcsh*) is used at the time of execution. For "static"
environment variables it not really important if they are escaped or not. But
for variables that are used inside the script at the time of execution
(e.g. ``msg``) they need to be escaped.

.. note::
   ``atd``  and  ``batch`` are not suitable when users are competing for
   resources.  If this is the case for your site,  you  might want to consider
   another batch system, such as
   `GNU Parallel <http://www.gnu.org/software/parallel/>`_.

Submission on a cluster
^^^^^^^^^^^^^^^^^^^^^^^
Various submission scripts can be created due to large veriety of cluster
configurations and job schedulers. Essentially, one needs to send UDP message
to the GUI run status server from compute node. For a start let's show required
update of sample ``itersubmit`` script that is actually executed at the
login node and may serve a as first check of network monitoring functionallity:

.. code-block:: diff
   :caption: QSUB.iter_coupled.orig QSUB.iter_coupled

   79c79,84
   < update_solps_run_status -n "Submitted at `date`"
   ---
   > set msg="Submitted at `date`"
   > update_solps_run_status -n ${msg}
   > if ($?SOLPS_GUI_IP) then
   >   echo ${USER} ${PWD} ${msg} \
   >       | nc -u -v -w 0 ${SOLPS_GUI_IP} ${SOLPS_GUI_PORT}
   > endif

When "the job" will start we need to receive UDP packet from the compute node
too. It is assumed and usually *environment variables* are preserved when the
job stars. Therefore *netcat* command is no different that with above
``itersubmit`` upgrade.

However, one may found out that the netcat command ``nc`` is not available
on the compute nodes. Furthermore access to *non-privileged ports*
on *login node* may be blocked by firewall of some kind.
To remedy the proble with *netcat* unavailability one may use
``solps-gui/src/utils/jobs_status/update_run_status`` netcat equivalent that
allows multiple destinations (broadcast for multiuser monitoring).

When the firewall blocks access from compute nodes to login node where
SOLPS GUI resides one may try to ssh back to login node by upgrading the
submitted script with:

.. code-block:: diff

   50c50,55
   < update_solps_run_status "Started on `hostname` at `date`"
   ---
   > set msg="Started on `hostname` at `date`"
   > update_solps_run_status ${msg}
   > if ($?SOLPS_GUI_IP) then
   >   ssh -o ConnectTimeout=10 ${USER}@${SOLPS_GUI_IP} \
   >   "echo ${USER} ${PWD} ${msg}|nc -u -v -w 0 ${SOLPS_GUI_IP} ${SOLPS_GUI_PORT}"
   > endif
   58c63,68
   < update_solps_run_status "Finished on `hostname` at `date`"
   ---
   > set msg="Finished on `hostname` at `date`"
   > update_solps_run_status ${msg}
   > if ($?SOLPS_GUI_IP) then
   >   ssh -o ConnectTimeout=10 ${USER}@${SOLPS_GUI_IP} \
   >   "echo ${USER} ${PWD} ${msg}|nc -u -v -w 0 ${SOLPS_GUI_IP} ${SOLPS_GUI_PORT}"
   > endif

This will usually work if key-only ssh access is enabled by the user. One may
even use more "secure" GUI server by using 127.0.0.1 localhost with ``nc``
update and bind GUI listening interface to 127.0.0.1 only.

To add login node to the list of know hosts users may need to run once::

    $ ssh-keygen -t rsa
    $ sh -c 'SOLPS_GUI_IP=$(hostname -i) \
    && SSH_KEY=$(ssh-keygen -F ${SOLPS_GUI_IP}) \
    && test -z "${SSH_KEY}" \
    && ssh-keyscan -t rsa -H ${SOLPS_GUI_IP} >> ~/.ssh/known_hosts'

Of course, recommended way of notifying the GUI is by direct update from
compute nodes by using *netcat* or ``update_run_status`` without remote
execution through secure shell.

For single users landing on a new cluster it is probably easier to update
just ``update_solps_run_status`` with the above script samples. Care is
needed that the updates are not then sent twice. That's why this shortcut
is not listed here. As usual, :abbr:`YMMV (your mileage may vary)`.
