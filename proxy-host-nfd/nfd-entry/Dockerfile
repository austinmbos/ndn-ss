From ndn-base
COPY . /app
WORKDIR /app
RUN make
EXPOSE 6363/udp

ENTRYPOINT ["/bin/bash"]
CMD ["./start.sh"]


