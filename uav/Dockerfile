FROM rust:1.71.1 as builder
WORKDIR /root
RUN cargo install --bins --examples --root /usr/local --version 0.17.3 dtn7
RUN cargo install --bins --examples --root /usr/local --version 0.6.1 dtn7-plus
RUN rustup component add rustfmt && cargo install --bins --examples --root /usr/local --version 0.1.3 coreemu

FROM px4io/px4-dev-simulation-focal:2022-08-12
LABEL Description="Docker image for network evaluations using px4 and gazebo"

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /root
#RUN mkdir -p /root/PX4-Autopilot
RUN git clone -j8 https://github.com/PX4/PX4-Autopilot
WORKDIR /root/PX4-Autopilot
RUN git checkout v1.13.2 && git submodule update --recursive
#RUN DONT_RUN=1 make px4_sitl gazebo___baylands
RUN DONT_RUN=1 no_sim=1 make px4_sitl gazebo

COPY --from=builder /usr/local/bin/* /usr/local/bin/
#COPY baylands /root/.gazebo/models/baylands

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install net-tools iproute2 iputils-ping vlan iptables ethtool babeld wget -y && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install mavproxy

#RUN mkdir -p /root/.gazebo/models
#WORKDIR /root/.gazebo/models
#RUN wget -r -l3 -np -R "index.html*" -R "*.tar.gz" -nH http://models.gazebosim.org/baylands/

COPY gz_pose.py /usr/local/bin

WORKDIR /root/PX4-Autopilot

COPY net.sh /net.sh
COPY net-routed.sh /net-routed.sh
