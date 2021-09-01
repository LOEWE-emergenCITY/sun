FROM rust:1.53 as builder
WORKDIR /root
RUN rustup component add rustfmt && cargo install --root /usr/local coreemu

FROM gh0st42/px4-emu

COPY --from=builder /usr/local/bin/core-pos /usr/local/bin/core-pos
COPY gz_pose.py /usr/local/bin

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install net-tools iproute2 iputils-ping vlan iptables ethtool babeld -y && \
    rm -rf /var/lib/apt/lists/*

COPY net.sh /net.sh 
COPY net-routed.sh /net-routed.sh

