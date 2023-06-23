FROM rust:1.61 as builder
WORKDIR /root
RUN rustup component add rustfmt
#RUN cargo install --bins --examples --root /usr/local --git https://github.com/dtn7/dtn7-rs --rev 7519b01 dtn7
#RUN cargo install --bins --examples --root /usr/local --git https://github.com/dtn7/dtn7-rs --rev 7519b01 examples
#RUN cargo install --bins --examples --root /usr/local --version 0.6.1 dtn7-plus
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y cmake \    
    && rm -rf /var/lib/apt/lists/*
RUN cargo install --bins --examples --root /usr/local --version 0.1.5 coreemu

FROM gh0st42/dtn7-showroom:v0.2.0

# install stuff for vnc session

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y lxde-core lxterminal \
    tightvncserver firefox wmctrl xterm \
    gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl \    
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/bin/* /usr/local/bin/

RUN touch /root/.Xresources
RUN touch /root/.Xauthority
WORKDIR /root
RUN mkdir -p .vnc Desktop

# mavproxy
RUN pip install mavproxy

# mesh routing
RUN apt-get update && \
    apt-get install babeld -y && \
    rm -rf /var/lib/apt/lists/*


# COPY xstartup with start for lxde
COPY xstartup /root/.vnc/
COPY coreemu.sh /root/Desktop

RUN mkdir -p /root/.core/myservices && mkdir -p /root/.coregui/custom_services && mkdir -p /root/.coregui/icons && mkdir -p /root/.coregui/backgrounds
COPY core_services/* /root/.core/myservices/
COPY coregui/config.yaml /root/.coregui/
COPY coregui/icons/* /root/.coregui/icons/
COPY coregui/backgrounds/* /root/.coregui/backgrounds/
COPY scripts/* /usr/local/bin/

COPY update-custom-services.sh /update-custom-services.sh
COPY Xdefaults /root/.Xdefaults

RUN echo "export USER=root" >> /root/.bashrc
ENV USER root
RUN printf "makitest\nmakitest\nn\n" | vncpasswd

COPY net.sh /net.sh 

EXPOSE 22
EXPOSE 5901
EXPOSE 50051

#WORKDIR /root
#RUN wget http://www.olsr.org/releases/0.9/olsrd-0.9.0.3.tar.bz2 && \
#tar xjf olsrd-0.9.0.3.tar.bz2 && \
#cd olsrd-0.9.0.3 && \
#make all && \
#cp olsrd /usr/local/bin && \
#rm -rf /root/olsrd-0.9.0.3.tar.bz2 /root/olsrd-0.9.0.3
