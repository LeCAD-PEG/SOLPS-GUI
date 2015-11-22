.. _tunneling-howto:

.. highlight:: csh

*************************
SOLPS-GUI Tunneling HOWTO
*************************

:Author: Leon Kos

GUI is designed to run in a graphical environment on a local workstation or
on a cluster with X11 environment. However, some cluster don't provide X11
desktop on a login node and for that running SOLPS-GUI is not native. If X11,
necesary Python and PyQt libraries are available on login node then the GUI
can be simply tunelled by adding ``-X`` or ``-Y`` switch when connecting to
login node with ``ssh``. Running SOLPS-GUI on a local machine for monitoring
purposes is possible too by tunneling UDP messages sent from compute nodes to
login node. In this HOWTO we'll access login node's network internal services
(UDP port 49406 ) with only SSH access to it. We will forward cluster
UDP traffic to TCP, then TCP traffic with the port-forwarding mechanism
of SSH to the other machine, then TCP to UDP/49406 on the other end.
Typically, you can do it with openvpn. But here, we'll do it with simpler
tools, only openssh and netcat. Here we are assuming that the SOLPS-GUI
is listening for UDP datagrams on non-privileged port 49406 which may
already be occupied by another user. In such situation on needs to select next
free port. Similar situation may occur when tunneling ports through ``ssh``.
That's why it is necessary for users to understand the tunelling and remote
execution.

Tunnelling Run status updates to local machine
==============================================

On your local machine (local), connect to the distant machine
(hpc-login4.iter.org) by SSH, with the additional -R option so that
SSH will TCP port-forward in reverse way as the server::

    local$ ssh -R 6667:localhost:6667 kosl@hpc-login4.iter.org

This will allow TCP connections on the port number 6666 on remote login node
to be forwarded to the port number 6666 on the local machine through
the secure channel.

In another shell on local machine we establish TCP to UDP transponder.
But first, we need to create a fifo. The fifo is necessary to have two-way
communication between the two channels. A simple shell pipe would only
communicate left process' standard output to right process' standard input.
Fifo makes this process cyclic. To prevent tunnel dropping after UDP client
disconnection ``-k`` switch is needed.::

   local$ mkfifo /tmp/fifo.${USER}
   local$ nc -v -k -l 6667 < /tmp/fifo.${USER} |
      nc -u -v localhost 49406 > /tmp/fifo.${USER}

On a cluster login node we just need to redirect UDP packets that we listen
on port 49406 to port 6667 so that can be forwarded to our server. As UDP
has no notion of :abbr:`EOT (End of Transfer)` *on a socket* it is necessary
that with ``-w0`` to break the connection after the received packet has been
forwarded. If the connection has *not* been broken, you may wait on a ``recv``
forever, because the socket will *not* tell you that there's nothing more to
read (for now).::

   [kosl@hpc-login4 ~]$ mkfifo /tmp/fifo.${USER}
   [kosl@hpc-login4 ~]$ nc -v localhost 6667 < /tmp/fifo.${USER} |
   nc -v -w0 -k -l 49406 -u > /tmp/fifo.${USER}

Finally, one can test the status update tunnel in SOLPS-GUI Log after issuing::

   [kosl@hpc-login4 ~]$ echo ${USER} ${PWD} status | nc -w0 -u localhost 49406

It should be noted that ``-l`` switch listens on all available network
interfaces and not just host-only localhost in above example. Compute nodes
should able to send run update to login node where monitoring GUI is
listening for UDP status updates.

Remote filesystem with SSHFS
----------------------------

Accessing remote filesystem of the cluster is possible with
`SSHFS <https://en.wikipedia.org/wiki/SSHFS>`_ and then mounted locally.


Sending Run status updates from compute nodes
=============================================

On many clusters network access from compute nodes to login node is not
blocked and one can simply use netcat or provided client ``update_run_status``
that is simple replacement for netcat with the following example usage within
the batch submission script::

   echo ${USER} ${PWD} status | ./update_run_status 10.153.0.16 49406

where ``10.153.0.16`` is the IP of the *hpc-login4* node.

On clusters that block backward connections from compute nodes to login node
unprivileged ports even though these are usually internal networks is
advisable that a system administrator changes iptables on login node
accordingly. In situation when opening ports is not possible one can issue
remote execution from client back to login node though available batch
submission channels used by :abbr:`MPI (Message Passing Interface)`. Most
commonly this means that ``ssh`` connection from the compute node to the
login node is possible. To be enable remote execution from the clients
one needs to have SSH keypair generated without password on the login node
and add it to known hosts by::

   [kosl@hpc-login4 ~]$ ssh-keygen -t rsa
   [kosl@hpc-login4 ~]$ test -z `ssh-keygen -F ${HOSTNAME}` \
        && ssh-keyscan -t rsa -H ${HOSTNAME} >> ~/.ssh/known_hosts
   [kosl@hpc-login4 ~]$ ssh localhost ls

After SSH keys verification, one can then test the batch submission update
inside the script with::

   ssh hpc-login4 "echo ${USER} ${PWD} status | nc -w0 -u localhost 49406"

Double quotes within the command mean that ``${USER} ${PWD}`` is replaced
at the compute node before actual ssh command is executed on login node.

