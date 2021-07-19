FROM gh0st42/coreemu-lab

RUN pip install mavproxy

RUN apt-get update && \
    apt-get install babeld -y && \
    rm -rf /var/lib/apt/lists/*

COPY net.sh /net.sh 

#WORKDIR /root
#RUN wget http://www.olsr.org/releases/0.9/olsrd-0.9.0.3.tar.bz2 && \
#tar xjf olsrd-0.9.0.3.tar.bz2 && \
#cd olsrd-0.9.0.3 && \
#make all && \
#cp olsrd /usr/local/bin && \
#rm -rf /root/olsrd-0.9.0.3.tar.bz2 /root/olsrd-0.9.0.3
