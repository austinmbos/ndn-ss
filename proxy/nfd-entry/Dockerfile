From nfd-base
COPY . /app
WORKDIR /app
RUN make
RUN echo 1 > shared/sym-dec.sem
RUN echo 1 > shared/sig-ver.sem
RUN echo 1 > shared/final.sem
EXPOSE 6363/udp

CMD ["./start.sh"]


