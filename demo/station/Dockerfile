FROM rust:1.61 as builder
WORKDIR /root
RUN rustup component add rustfmt
RUN cargo install --bins --examples --root /usr/local --git https://github.com/dtn7/dtn7-rs --rev 7519b01 dtn7
RUN cargo install --bins --examples --root /usr/local --git https://github.com/dtn7/dtn7-rs --rev 7519b01 examples
RUN cargo install --bins --examples --root /usr/local --version 0.6.1 dtn7-plus
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y cmake \    
    && rm -rf /var/lib/apt/lists/*
RUN cargo install --bins --examples --root /usr/local --version 0.1.5 coreemu

FROM ubuntu:focal-20220426
RUN  apt-get update

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y lxde-core lxterminal
RUN apt-get -y install tightvncserver firefox nano wmctrl iproute2 \
    gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl \
    wget sudo less net-tools iputils-ping babeld libx11-xcb1 libxcb-xinerama0 && \
    apt-get remove modemmanager -y && rm -rf /var/lib/apt/lists/*

# files for VNC
RUN touch /root/.Xresources
RUN touch /root/.Xauthority
WORKDIR /root
RUN mkdir .vnc

RUN useradd test && \
    usermod -a -G dialout test && \
    mkdir /home/test && \
    chown test /home/test

RUN mkdir /apps && cd /apps &&\
    wget https://s3-us-west-2.amazonaws.com/qgroundcontrol/latest/QGroundControl.AppImage && \
    chmod a+x QGroundControl.AppImage && \
    chown test /apps && \
    sudo -u test ./QGroundControl.AppImage --appimage-extract && \
    mkdir /root/Desktop

COPY --from=builder /usr/local/bin/* /usr/local/bin/

RUN apt-get update
RUN apt-get install -y python3-pip tcpdump
RUN pip3 install mavsdk mavproxy

COPY missions/* /home/test/

# COPY xstartup with start for lxde
COPY xstartup /root/.vnc/
COPY qgc.sh /usr/local/bin
COPY qgc.sh /root/Desktop

RUN echo "export USER=root" >> /root/.bashrc
ENV USER root
# COPY script. removes Lock files and start tightvncserver
COPY entrypoint.sh /entrypoint.sh
# set password
RUN printf "makitest\nmakitest\nn\n" | vncpasswd

RUN mkdir -p /home/test/.config/QGroundControl.org
COPY QGroundControl.ini /home/test/.config/QGroundControl.org
COPY xstartup /root/.vnc/

COPY net.sh /net.sh 
COPY net-routed.sh /net-routed.sh

EXPOSE 5901
ENTRYPOINT ["/entrypoint.sh" ]







