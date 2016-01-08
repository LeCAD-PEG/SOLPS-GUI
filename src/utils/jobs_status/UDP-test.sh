#!/bin/sh
# This utility tests possibility of sending UDP messages from compute nodes
# back to login node from which batch jobs are submitted. 
# Firstly it demostrates how netcat utility works on login node and then
# submits the job to node and waits for an message 
# It should print "Hello from compute node". Otherwise may wait forever.
#

PORT=44354 # non-privileded port numbers are from 1024 to 65535
LOGIN_NODE_IP=$(hostname -i)
SYSTEM_NC=$(which nc)

cp  ${SYSTEM_NC} ${HOME}
${HOME}/nc -lvu ${LOGIN_NODE_IP} ${PORT} & 
echo "Hello from login node" | ${HOME}/nc -uvw0 ${LOGIN_NODE_IP} ${PORT}
sleep 5

echo "Submitting test to compute node"
cat <<EOF | qsub -N UDP-test -o UDP-test.log -e UDP-test.err
sleep 5
echo "Hello from compute node" | ${HOME}/nc -uvw0 ${LOGIN_NODE_IP} ${PORT}
echo "You should receive hello on ${LOGIN_NODE_IP} ${PORT}"
EOF

echo "Waiting for UDP message from compute node..."
${HOME}/nc -lvu ${LOGIN_NODE_IP} ${PORT}

