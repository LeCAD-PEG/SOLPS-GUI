.. _setup:

.. highlight:: csh

********************************
Setting up SOLPS GUI environment
********************************

Creating SSH host keys
======================

    $ sh -c 'SOLPS_GUI_IP=$(hostname -i) \
    && SSH_KEY=$(ssh-keygen -F ${SOLPS_GUI_IP}) \
    && test -z "${SSH_KEY}" \
    && ssh-keyscan -t rsa -H ${SOLPS_GUI_IP} >> ~/.ssh/known_hosts'


ITER
====

   module use /work/imas/etc/modulefiles
   module load solps-gui
