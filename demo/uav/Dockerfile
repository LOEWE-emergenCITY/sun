FROM rust:1.61 as builder
WORKDIR /root
RUN cargo install --bins --examples --root /usr/local --version 0.17.3 dtn7
RUN cargo install --bins --examples --root /usr/local --version 0.6.1 dtn7-plus
RUN rustup component add rustfmt && cargo install --root /usr/local --version 0.1.3 coreemu

FROM gh0st42/px4-emu

COPY --from=builder /usr/local/bin/core-pos /usr/local/bin/core-pos
COPY gz_pose.py /usr/local/bin

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install net-tools iproute2 iputils-ping vlan iptables ethtool babeld -y && \
    rm -rf /var/lib/apt/lists/*

COPY net.sh /net.sh 
COPY net-routed.sh /net-routed.sh

