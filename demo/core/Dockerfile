FROM rust:1.61 as builder
WORKDIR /root
RUN cargo install --bins --examples --root /usr/local --version 0.17.3 dtn7
RUN cargo install --bins --examples --root /usr/local --version 0.6.1 dtn7-plus

FROM gh0st42/coreemu-lab:coreemu7

# install stuff for vnc session

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y lxde-core lxterminal \
    tightvncserver firefox wmctrl \
    gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl \    
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/bin/* /usr/local/bin/

RUN touch /root/.Xresources
RUN touch /root/.Xauthority
WORKDIR /root
RUN mkdir .vnc Desktop

# mavproxy
RUN pip install mavproxy

# mesh routing
RUN apt-get update && \
    apt-get install babeld -y && \
    rm -rf /var/lib/apt/lists/*


# COPY xstartup with start for lxde
COPY xstartup /root/.vnc/
COPY coreemu.sh /root/Desktop

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
