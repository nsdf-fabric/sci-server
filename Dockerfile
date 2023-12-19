
# see https://github.com/sciserver/sciserver-compute-images/tree/master/essentials/3.0/sciserver-jupyter

FROM ubuntu:22.04

RUN useradd -m idies \
    && mkdir /home/idies/workspace \
    && chown idies:idies /home/idies/workspace

ARG DEBIAN_FRONTEND=noninteractive

RUN ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime \
    && apt-get update \
    && apt-get install -y \
        build-essential \
        cmake \
        sudo \
        wget \
        curl \
        git \
        vim \
        htop \
        locales \
    && rm -rf /var/lib/apt/lists/* \
    && locale-gen "en_US.UTF-8" \
    && update-locale "LANG=en_US.UTF-8"

# RUN apt-get update \
#    && apt-get install -y texlive-full \
#    && rm -rf /var/lib/apt/lists/*

EXPOSE 8888

# RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
#     && apt-get update \
#    && apt-get install -y \
#        nodejs \
#        yarn \
#    && rm -rf /var/lib/apt/lists/*

USER idies

WORKDIR /home/idies

RUN curl -L "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh" -o miniforge3.sh \
    && bash miniforge3.sh -b \
    && rm -f miniforge3.sh

ENV PATH /home/idies/miniforge3/bin:$PATH

COPY requirements.txt ./requirements.txt

RUN mamba install -y -c conda-forge --file requirements.txt

COPY startup.sh ./startup.sh

ENV SHELL /bin/bash
