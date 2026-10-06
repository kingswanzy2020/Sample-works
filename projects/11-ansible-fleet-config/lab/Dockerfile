# A lab "server": Ubuntu with SSH and Python, so Ansible manages it like a real host.
# Containers share the host kernel: kernel-level settings (sysctl, boot params) need VMs. See README.
FROM ubuntu:24.04
RUN apt-get update \
 && apt-get install -y --no-install-recommends openssh-server python3 sudo ca-certificates procps \
 && rm -rf /var/lib/apt/lists/* \
 && useradd -m -s /bin/bash ops \
 && echo "ops ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ops \
 && mkdir -p /run/sshd /home/ops/.ssh && chown ops:ops /home/ops/.ssh && chmod 700 /home/ops/.ssh \
 && sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
COPY --chmod=755 entrypoint.sh /entrypoint.sh
EXPOSE 22
ENTRYPOINT ["/entrypoint.sh"]
