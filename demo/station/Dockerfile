FROM gh0st42/qgc_vnc

RUN mkdir -p /home/test/.config/QGroundControl.org
COPY QGroundControl.ini /home/test/.config/QGroundControl.org

#RUN apt-get update && \
#apt-get install -y && \
#rm -rf /var/lib/apt/lists/*

COPY net.sh /net.sh 

