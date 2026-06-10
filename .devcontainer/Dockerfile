FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    pkg-config \
    curl \
    wget \
    python3-dev \
    python3-pip \
    python3-venv \
    libeigen3-dev \
    libopencv-dev \
    libssl-dev \
    libboost-all-dev \
    libopengl-dev \
    libegl1-mesa-dev \
    libgl1-mesa-dev \
    libglew-dev \
    libepoxy-dev \
    libx11-dev \
    libxrandr-dev \
    libxinerama-dev \
    libxcursor-dev \
    libxi-dev \
    usbutils \
    && rm -rf /var/lib/apt/lists/*
RUN usermod -aG video,plugdev,dialout vscode

USER vscode

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/home/vscode/.local/bin:${PATH}"

RUN uv python install 3.12
RUN uv venv --python 3.12 /home/vscode/.venv

ENV VIRTUAL_ENV=/home/vscode/.venv
ENV PATH="/home/vscode/.venv/bin:${PATH}"

RUN uv pip install pyrealsense2 numpy scipy viser