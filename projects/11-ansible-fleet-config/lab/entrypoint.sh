#!/bin/sh
# Install the lab public key (mounted read-only) for the ops user, then run sshd in the foreground.
set -e
cp /lab-key.pub /home/ops/.ssh/authorized_keys
chown ops:ops /home/ops/.ssh/authorized_keys
chmod 600 /home/ops/.ssh/authorized_keys
ssh-keygen -A >/dev/null
exec /usr/sbin/sshd -D -e
