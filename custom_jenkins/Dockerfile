# Use the official Jenkins LTS image as the base
FROM jenkins/jenkins:lts

# Switch to root to install system packages
USER root

# 1. Install prerequisites (excluding software-properties-common which is unavailable)
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    && install -m 0755 -d /etc/apt/keyrings

# 2. Add Docker's official GPG key (Modern secure method)
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && chmod a+r /etc/apt/keyrings/docker.gpg

# 3. Set up the Docker repository dynamically based on the OS version
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

# 4. Install Docker CLI and Engine components
RUN apt-get update && apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 5. Give the 'jenkins' user access to the docker group
# This allows Jenkins to run docker commands if the socket is mounted
RUN usermod -aG docker jenkins

# Switch back to the Jenkins user
USER jenkins