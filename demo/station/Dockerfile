FROM rust:1.61 as builder
WORKDIR /root
RUN cargo install --bins --examples --root /usr/local --version 0.17.3 dtn7
RUN cargo install --bins --examples --root /usr/local --version 0.6.1 dtn7-plus

FROM gh0st42/qgc_vnc

RUN mkdir -p /home/test/.config/QGroundControl.org
COPY QGroundControl.ini /home/test/.config/QGroundControl.org

RUN apt-get update && \
    apt-get install -y wmctrl && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y babeld && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/bin/* /usr/local/bin/

RUN printf "makitest\nmakitest\nn\n" | vncpasswd

COPY xstartup /root/.vnc/

EXPOSE 5901

COPY net.sh /net.sh 
COPY net-routed.sh /net-routed.sh