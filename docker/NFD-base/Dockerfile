FROM ndn-base
COPY test.sh /
WORKDIR /
RUN chmod +x test.sh
RUN bash test.sh
COPY nfd-start /usr/local/bin/
COPY nfd-stop /usr/local/bin
ENTRYPOINT ["/bin/bash"]

# pass in CMD [""] here for command to execute on container run

